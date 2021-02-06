#include <torch/torch.h>
#include <vector>
#include <math.h>

enum STATUS {
    PLAYING,
    WON,
    LOST,
    RESETTING
};

struct TestEnvironment
{
    std::vector<double> pos_;
    std::vector<double> goal_;
    std::vector<double> state_;

    double old_dist_;

    TestEnvironment(double x, double y)
    {
        goal_ = {x, y};
        pos_ = {0, 0};
        state_ = {pos_[0], pos_[1], goal_[0], goal_[1]};  

        old_dist_ = GoalDist(pos_);
    };

    auto Act(double act_x, double act_y) -> std::tuple<torch::Tensor, int, torch::Tensor>
    { 
        old_dist_ = GoalDist(pos_);

        double max_step = 0.1;
        pos_[0] += max_step*act_x;
        pos_[1] += max_step*act_y;

        state_ = {pos_[0], pos_[1], goal_[0], goal_[1]};

        torch::Tensor state = State();
        torch::Tensor done = torch::zeros({1, 1}, torch::kF64);
        STATUS status;

        if (GoalDist(pos_) < 6e-1) {
            status = WON;
            done[0][0] = 1.;
        }
        else if (GoalDist(pos_) > 1e1) {
            status = LOST;
            done[0][0] = 1.;
        }
        else {
            status = PLAYING;
            done[0][0] = 0.;
        }

        return std::make_tuple(state, status, done);
    }
    auto State() -> torch::Tensor
    {
        torch::Tensor state = torch::zeros({1, static_cast<int>(state_.size())}, torch::kF64);
        std::memcpy(state.data_ptr(), state_.data(), state_.size()*sizeof(double));
        return state;
    }    
    auto Reward(int status) -> torch::Tensor
    {
        torch::Tensor reward = torch::full({1, 1}, old_dist_ - GoalDist(pos_), torch::kF64);
        
        switch (status)
        {
            case PLAYING:
                break;
            case WON:
                reward[0][0] += 10.;
                printf("won, reward: %f\n", reward[0][0].item<double>());
                break;
            case LOST:
                reward[0][0] -= 10.;
                printf("lost, reward: %f\n", reward[0][0].item<double>());
                break;
        }

        return reward;
    }
    double GoalDist(std::vector<double>& x) 
    { 
        return sqrt( pow((goal_[0]-x[0]), 2.0) + pow((goal_[1]-x[1]), 2.0) );
    }
    void Reset()
    {
        pos_={0,0};
        state_ = {pos_[0], pos_[1], goal_[0], goal_[1]};
    }
    void SetGoal(double x, double y)
    {
        goal_[0] = x;
        goal_[1] = y;

        old_dist_ = GoalDist(pos_);
        state_ = {pos_[0], pos_[1], goal_[0], goal_[1]};
    }
};