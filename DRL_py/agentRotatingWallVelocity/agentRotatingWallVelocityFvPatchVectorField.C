/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2011-2016 OpenFOAM Foundation
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "agentRotatingWallVelocityFvPatchVectorField.H"
#include "addToRunTimeSelectionTable.H"
#include "volFields.H"
#include "surfaceFields.H"

// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::agentRotatingWallVelocityFvPatchVectorField::
    agentRotatingWallVelocityFvPatchVectorField(
        const fvPatch &p,
        const DimensionedField<vector, volMesh> &iF)
    : fixedValueFvPatchField<vector>(p, iF),
      origin_(),
      axis_(Zero)
{
}

Foam::agentRotatingWallVelocityFvPatchVectorField::
    agentRotatingWallVelocityFvPatchVectorField(
        const fvPatch &p,
        const DimensionedField<vector, volMesh> &iF,
        const dictionary &dict)
    : fixedValueFvPatchField<vector>(p, iF, dict, false),
      origin_(dict.get<vector>("origin")),
      axis_(dict.get<vector>("axis")),
      train_(dict.get<bool>("train")),
      interval_(dict.get<int>("interval")),
      start_time_(dict.get<scalar>("startTime")),
      start_iter_(0),
      policy_name_(dict.get<word>("policy")),
      policy_(torch::jit::load(policy_name_)),
      abs_omega_max_(dict.get<scalar>("absOmegaMax")),
      log_std_max_(dict.get<scalar>("logStdMax")),
      omega_(0.0),
      omega_old_(0.0),
      control_time_(0.0),
      theta_cumulative_(0.0),
      dt_theta_cumulative_(0.0)
{
    if (dict.found("value"))
    {
        fvPatchField<vector>::operator=(
            vectorField("value", dict, p.size()));
    }
    else
    {
        // Evaluate the wall velocity
        updateCoeffs();
    }
}

Foam::agentRotatingWallVelocityFvPatchVectorField::
    agentRotatingWallVelocityFvPatchVectorField(
        const agentRotatingWallVelocityFvPatchVectorField &ptf,
        const fvPatch &p,
        const DimensionedField<vector, volMesh> &iF,
        const fvPatchFieldMapper &mapper)
    : fixedValueFvPatchField<vector>(ptf, p, iF, mapper),
      origin_(ptf.origin_),
      axis_(ptf.axis_)
{
}

Foam::agentRotatingWallVelocityFvPatchVectorField::
    agentRotatingWallVelocityFvPatchVectorField(
        const agentRotatingWallVelocityFvPatchVectorField &rwvpvf)
    : fixedValueFvPatchField<vector>(rwvpvf),
      origin_(rwvpvf.origin_),
      axis_(rwvpvf.axis_)
{
}

Foam::agentRotatingWallVelocityFvPatchVectorField::
    agentRotatingWallVelocityFvPatchVectorField(
        const agentRotatingWallVelocityFvPatchVectorField &rwvpvf,
        const DimensionedField<vector, volMesh> &iF)
    : fixedValueFvPatchField<vector>(rwvpvf, iF),
      origin_(rwvpvf.origin_),
      axis_(rwvpvf.axis_)
{
}

// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void Foam::agentRotatingWallVelocityFvPatchVectorField::updateCoeffs()
{
    if (updated())
    {
        return;
    }

    // update angular velocity
    const scalar t = this->db().time().timeOutputValue();
    bool steps_remaining = (this->db().time().timeIndex() - start_iter_) % interval_ == 0;
    if (t >= start_time_)
    {
        if(start_iter_ == 0)
        {
            start_iter_ = this->db().time().timeIndex();
            steps_remaining = true;
        }
        if (steps_remaining && update_omega_)
        {
            Info << "Updating Omega with policy.\n";
            omega_old_ = omega_;
            control_time_ = t;
            // creating the feature vector
            const fvPatchField<scalar> &p = patch().lookupPatchField<volScalarField, scalar>("p");
            torch::Tensor features = torch::zeros({1, p.size()}, torch::kFloat64);
            forAll(p, i)
            {
                features[0][i] = p[i];
            }
            std::vector<torch::jit::IValue> policyFeatures{features};
            torch::Tensor gauss_parameters = policy_.forward(policyFeatures).toTensor();
            torch::Tensor mean_tensor = gauss_parameters[0][0];
            std::cout << "log_std: " << gauss_parameters[0][1].item<double>() << "\n";
            torch::Tensor log_std_tensor = torch::clamp(gauss_parameters[0][1], -20.0, log_std_max_);
            std::cout << "clipped log_std: " << log_std_tensor << "\n";
            if (train_)
            {
                // sample from Gaussian distribution during training
                omega_ = at::normal(mean_tensor, log_std_tensor.exp()).item<double>();
            }
            else
            {
                // use expected (mean) angular velocity
                omega_ = mean_tensor.item<double>();
            }
            // avoid update of angular velocity during p-U coupling
            update_omega_ = false;
            // save trajectory
            scalar mean = mean_tensor.item<double>();
            scalar log_std = log_std_tensor.item<double>();
            scalar var = (log_std_tensor + log_std_tensor).exp().item<double>();
            scalar entropy = 0.5 + 0.5*log(2.0*M_PI) + log_std;
            scalar log_p = -((omega_ - mean) * (omega_ - mean)) / (2.0*var) - log_std - log(sqrt(2.0*M_PI));
            saveTrajectory(log_p, entropy, mean, log_std);
            // reset cumulative values
            theta_cumulative_ = 0.0;
            dt_theta_cumulative_ = 0.0;
            Info << "New omega: " << omega_ << "; old value: " << omega_old_ << "\n";
        }
    }

    // activate update of angular velocity after p-U coupling
    if (!steps_remaining)
    {
        update_omega_ = true;
    }

    // update angular velocity by linear transition from old to new value
    const scalar dt = this->db().time().deltaTValue();
    scalar d_omega = (omega_ - omega_old_) / (dt * interval_) * (t - control_time_);
    scalar omega = omega_old_ + d_omega;
    theta_cumulative_ += abs(omega) * dt;
    dt_theta_cumulative_ += abs(omega);

    // Calculate the rotating wall velocity from the specification of the motion
    const vectorField Up(
        (-omega) * ((patch().Cf() - origin_) ^ (axis_ / mag(axis_))));

    // Remove the component of Up normal to the wall
    // just in case it is not exactly circular
    const vectorField n(patch().nf());
    vectorField::operator=(Up - n * (n & Up));

    fixedValueFvPatchVectorField::updateCoeffs();
}

void Foam::agentRotatingWallVelocityFvPatchVectorField::write(Ostream &os) const
{
    fvPatchVectorField::write(os);
    os.writeEntry("origin", origin_);
    os.writeEntry("axis", axis_);
    writeEntry("value", os);
}

void Foam::agentRotatingWallVelocityFvPatchVectorField::saveTrajectory(scalar log_p, scalar entropy, scalar mean, scalar log_std) const
{
    std::ifstream file("trajectory.csv");
    std::fstream trajectory("trajectory.csv", std::ios::app);
    const scalar t = this->db().time().timeOutputValue();
    const fvPatchField<scalar> &p = patch().lookupPatchField<volScalarField, scalar>("p");
    if(!file.good())
    {
        // write header
        trajectory << "t, omega, omega_mean, omega_log_std, log_prob, entropy, theta_sum, dt_theta_sum, p(" << p.size() << ")";
    }
    trajectory << std::setprecision(15)
               << "\n"
               << t << ", "
               << omega_ << ", "
               << mean << ", "
               << log_std << ", "
               << log_p << ", "
               << entropy << ", "
               << theta_cumulative_ << ", "
               << dt_theta_cumulative_;
    
    forAll(p, i)
    {
            trajectory << ", " << p[i];
    }
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{
    makePatchTypeField(
        fvPatchVectorField,
        agentRotatingWallVelocityFvPatchVectorField);
}

// ************************************************************************* //
