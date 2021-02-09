
class EpisodeBuffer:

    def fill(self):
        # fill the memory of variable present in get_stack
        pass

    def get_stacks(self):
        return (self.states_mem, self.actions_mem,
                self.returns_mem, self.gaes_mem, self.logpas_mem)

    def __len__(self):
        return self.episode_steps[self.episode_steps > 0].sum()
