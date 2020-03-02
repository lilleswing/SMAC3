import contextlib
import shutil
import unittest.mock

from ConfigSpace.hyperparameters import UniformFloatHyperparameter

from smac.configspace import ConfigurationSpace

from smac.facade.smac_bohb_facade import BOHB4HPO
from smac.initial_design.random_configuration_design import RandomConfigurations
from smac.scenario.scenario import Scenario


class TestSMACFacade(unittest.TestCase):

    def setUp(self):
        self.cs = ConfigurationSpace()
        self.scenario = Scenario({'cs': self.cs, 'run_obj': 'quality',
                                  'output_dir': ''})
        self.output_dirs = []

    def tearDown(self):
        for i in range(20):
            with contextlib.suppress(Exception):
                dirname = 'run_1' + ('.OLD' * i)
                shutil.rmtree(dirname)
        for output_dir in self.output_dirs:
            if output_dir:
                shutil.rmtree(output_dir, ignore_errors=True)

    def test_initializations(self):
        cs = ConfigurationSpace()
        for i in range(40):
            cs.add_hyperparameter(UniformFloatHyperparameter('x%d' % (i + 1), 0, 1))
        scenario = Scenario({'cs': cs, 'run_obj': 'quality'})
        hb_kwargs = {'initial_budget': 1, 'max_budget': 3}
        facade = BOHB4HPO(scenario=scenario, intensifier_kwargs=hb_kwargs)

        self.assertIsInstance(facade.solver.initial_design, RandomConfigurations)
        # ensure number of samples required is D+1
        self.assertEqual(facade.solver.epm_chooser.min_samples_model, 41)
        self.output_dirs.append(scenario.output_dir)
