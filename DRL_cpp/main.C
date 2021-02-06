#include <fstream>
#include <torch/torch.h>
#include <random>
#include "network.h"
#include "Testenv.h"
#include "hyperparameters.h"
#include "ppo.h"

int main() {

    // Random engine.
    std::random_device rd;
    std::mt19937 re(rd());
    std::uniform_int_distribution<> dist(-5, 5);

    //hyperparameters
    hyperparameters hyp;

    // Environment.
    double x = double(dist(re)); // goal x pos
    double y = double(dist(re)); // goal y pos
    TestEnvironment  env(x, y);

    // Model.
    uint n_in = 4;
    uint n_out = 2;
    double std = 1e-2;

    NN_model nn_ac(n_in, n_out, std);
    nn_ac->to(torch::kF64);
    nn_ac->normal(0., std);
    torch::optim::Adam opt(nn_ac->parameters(), 1e-3);

    // Output.
    std::ofstream out;
    out.open("../data/data.csv");

    // episode, agent_x, agent_y, goal_x, goal_y, STATUS=(PLAYING, WON, LOST, RESETTING)
    std::cout << 1 << ", " << env.pos_[0] << ", " << env.pos_[1] << ", " << env.goal_[0] << ", " << env.goal_[1] << ", " << RESETTING << "\n";

    PPO::learn_agent(nn_ac, env, hyp, opt, out);

    out.close();

    return 0;
}
