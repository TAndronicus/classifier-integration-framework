import unittest

from ClassifierData import ClassifierData


class ClassifierDataTest(unittest.TestCase):

    def test_validate_type_of_classifier(self):
        # given
        type_of_classifier = 'test'
        # when
        classifier_data = ClassifierData(type_of_classifier = type_of_classifier)
        # then
        with self.assertRaisesRegex(Exception, 'type_of_classifier must be of type ClfType'):
            classifier_data.validate_type_of_classifier()

    def test_validate_are_samples_generated(self):
        # given
        are_samples_generated = 'test'
        # when
        classifier_data = ClassifierData(are_samples_generated = are_samples_generated)
        # then
        with self.assertRaisesRegex(Exception, 'are_samples_generated must be of type boolean'):
            classifier_data.validate_are_samples_generated()

    def test_validate_number_of_samples_if_generated_non_int(self):
        # given
        number_of_samples_if_generated = 'test'
        # when
        classifier_data = ClassifierData(number_of_samples_if_generated = number_of_samples_if_generated)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_samples_if_generated must be of type int'):
            classifier_data.validate_number_of_samples_if_generated()

    def test_validate_number_of_samples_if_generated_too_low(self):
        # given
        number_of_samples_if_generated = ClassifierData.MINIMAL_NUMBER_OF_SAMPLES - 1
        # when
        classifier_data = ClassifierData(number_of_samples_if_generated = number_of_samples_if_generated)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_samples_if_generated must be at least'):
            classifier_data.validate_number_of_samples_if_generated()

    def test_validate_number_of_dataset_if_not_generated_non_int(self):
        # given
        number_of_dataset_if_not_generated = 'test'
        # when
        classifier_data = ClassifierData(number_of_dataset_if_not_generated = number_of_dataset_if_not_generated)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_dataset_if_not_generated must be of type int'):
            classifier_data.validate_number_of_dataset_if_not_generated()

    def test_validate_number_of_dataset_if_not_generated_too_low(self):
        # given
        number_of_dataset_if_not_generated = -1
        # when
        classifier_data = ClassifierData(number_of_dataset_if_not_generated = number_of_dataset_if_not_generated)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_dataset_if_not_generated must be positive'):
            classifier_data.validate_number_of_dataset_if_not_generated()

    def test_validate_switch_columns_while_loading(self):
        # given
        switch_columns_while_loading = 'test'
        # when
        classifier_data = ClassifierData(switch_columns_while_loading = switch_columns_while_loading)
        # then
        with self.assertRaisesRegex(Exception, 'switch_columns_while_loading must be of type boolean'):
            classifier_data.validate_switch_columns_while_loading()

    def test_validate_space_division_empty(self):
        # given
        space_division = []
        # when
        classifier_data = ClassifierData(space_division = space_division)
        # then
        with self.assertRaisesRegex(Exception, 'space_division must have elements'):
            classifier_data.validate_space_division()

    def test_validate_space_division_non_int(self):
        # given
        space_division = [.5]
        # when
        classifier_data = ClassifierData(space_division = space_division)
        # then
        with self.assertRaisesRegex(Exception, 'space_division elements must be of type int'):
            classifier_data.validate_space_division()

    def test_validate_space_division_non_positive(self):
        # given
        space_division = [-1]
        # when
        classifier_data = ClassifierData(space_division = space_division)
        # then
        with self.assertRaisesRegex(Exception, 'space_division elements must be positive'):
            classifier_data.validate_space_division()

    def test_validate_number_of_space_parts_non_int(self):
        # given
        number_of_space_parts = 'test'
        # when
        classifier_data = ClassifierData(number_of_space_parts = number_of_space_parts)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_space_parts must be of type int'):
            classifier_data.validate_number_of_space_parts()

    def test_validate_number_of_space_parts_too_low(self):
        # given
        number_of_space_parts = -1
        # when
        classifier_data = ClassifierData(number_of_space_parts = number_of_space_parts)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_space_parts must be positive'):
            classifier_data.validate_number_of_space_parts()

    def test_validate_number_of_classifiers_non_int(self):
        # given
        number_of_classifiers = 'test'
        # when
        classifier_data = ClassifierData(number_of_classifiers = number_of_classifiers)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_classifiers must be of type int'):
            classifier_data.validate_number_of_classifiers()

    def test_validate_number_of_classifiers_too_low(self):
        # given
        number_of_classifiers = -1
        # when
        classifier_data = ClassifierData(number_of_classifiers = number_of_classifiers)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_classifiers must be positive'):
            classifier_data.validate_number_of_classifiers()

    def test_validate_number_of_best_classifiers_non_int(self):
        # given
        number_of_best_classifiers = 'test'
        # when
        classifier_data = ClassifierData(number_of_best_classifiers = number_of_best_classifiers)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_best_classifiers must be of type int'):
            classifier_data.validate_number_of_best_classifiers()

    def test_validate_number_of_best_classifiers_too_low(self):
        # given
        number_of_best_classifiers = -1
        # when
        classifier_data = ClassifierData(number_of_best_classifiers = number_of_best_classifiers)
        # then
        with self.assertRaisesRegex(Exception, 'number_of_best_classifiers must be positive'):
            classifier_data.validate_number_of_best_classifiers()

    def test_validate_draw_color_plot(self):
        # given
        draw_color_plot = 'test'
        # when
        classifier_data = ClassifierData(show_color_plot = draw_color_plot)
        # then
        with self.assertRaisesRegex(Exception, 'draw_color_plot must be of type boolean'):
            classifier_data.validate_draw_color_plot()

    def test_validate_write_computed_scores(self):
        # given
        write_computed_scores = 'test'
        # when
        classifier_data = ClassifierData(write_computed_scores = write_computed_scores)
        # then
        with self.assertRaisesRegex(Exception, 'write_computed_scores must be of type boolean'):
            classifier_data.validate_write_computed_scores()

    def test_validate_show_plots(self):
        # given
        show_plots = 'test'
        # when
        classifier_data = ClassifierData(show_plots = show_plots)
        # then
        with self.assertRaisesRegex(Exception, 'show_plots must be of type boolean'):
            classifier_data.validate_show_plots()

    def test_validate_show_only_first_plot(self):
        # given
        show_only_first_plot = 'test'
        # when
        classifier_data = ClassifierData(show_only_first_plot = show_only_first_plot)
        # then
        with self.assertRaisesRegex(Exception, 'show_only_first_plot must be of type boolean'):
            classifier_data.validate_show_only_first_plot()

    def test_validate_columns_non_matrix(self):
        # given
        columns = 'test'
        # when
        classifier_data = ClassifierData(columns = columns)
        # then
        with self.assertRaisesRegex(Exception, 'Columns must be vector of size 1 x 2'):
            classifier_data.validate_columns()

    def test_validate_columns_non_ints(self):
        # given
        columns = ['test', 'test']
        # when
        classifier_data = ClassifierData(columns = columns)
        # then
        with self.assertRaisesRegex(Exception, 'Elements of columns must be of type int'):
            classifier_data.validate_columns()

    def test_validate_columns_non_positive(self):
        # given
        columns = [-1, -1]
        # when
        classifier_data = ClassifierData(columns = columns)
        # then
        with self.assertRaisesRegex(Exception, 'Column number must be positive'):
            classifier_data.validate_columns()

    def test_validate_columns_not_different(self):
        # given
        columns = [1, 1]
        # when
        classifier_data = ClassifierData(columns = columns)
        # then
        with self.assertRaisesRegex(Exception, 'Elements of matrix must be different'):
            classifier_data.validate_columns()

    def test_validate_is_validation_hard(self):
        # given
        is_validation_hard = 'test'
        # when
        classifier_data = ClassifierData(is_validation_hard = is_validation_hard)
        # then
        with self.assertRaisesRegex(Exception, 'is_validation_hard must be of type boolean'):
            classifier_data.validate_is_validation_hard()

    def test_validate_filename(self):
        # given
        filename = 0
        # when
        classifier_data = ClassifierData(filename = filename)
        # then
        with self.assertRaisesRegex(Exception, 'filename must be of type str'):
            classifier_data.validate_filename()

    def test_validate_generate_all_permutations(self):
        # given
        generate_all_permutations = 'test'
        # when
        classifier_data = ClassifierData(generate_all_permutations = generate_all_permutations)
        # then
        with self.assertRaisesRegex(Exception, 'generate_all_permutations must be of type bool'):
            classifier_data.validate_generate_all_permutations()

    def test_validate_log_number(self):
        # given
        log_number = 'test'
        # when
        classifier_data = ClassifierData(log_number = log_number)
        # then
        with self.assertRaisesRegex(Exception, 'log_number must be of type int'):
            classifier_data.validate_log_number()

    def test_validate_bagging(self):
        # given
        bagging = 'test'
        # when
        classifier_data = ClassifierData(bagging = bagging)
        # then
        with self.assertRaisesRegex(Exception, 'bagging must be of type bool'):
            classifier_data.validate_bagging()

    def test_validate_logging_to_file(self):
        # given
        logging_to_file = 'test'
        # when
        classifier_data = ClassifierData(logging_to_file = logging_to_file)
        # then
        with self.assertRaisesRegex(Exception, 'logging_to_file must be of type bool'):
            classifier_data.validate_logging_to_file()

    def test_validate_logging_intermediate_results(self):
        # given
        logging_intermediate_results = 'test'
        # when
        classifier_data = ClassifierData(logging_intermediate_results = logging_intermediate_results)
        # then
        with self.assertRaisesRegex(Exception, 'logging_intermediate_results must be of type bool'):
            classifier_data.validate_logging_intermediate_results()

    def test_validate_minimum(self):
        # given
        minimum = 'test'
        # when
        classifier_data = ClassifierData(minimum = minimum)
        # then
        with self.assertRaisesRegex(Exception, 'minimum must be of type float'):
            classifier_data.validate_minimum()

    def test_validate_maximum(self):
        # given
        maximum = 'test'
        # when
        classifier_data = ClassifierData(maximum = maximum)
        # then
        with self.assertRaisesRegex(Exception, 'maximum must be of type float'):
            classifier_data.validate_maximum()


    def test_validate_type_of_composition(self):
        # given
        type_of_composition = 'test'
        # when
        classifier_data = ClassifierData(type_of_composition = type_of_composition)
        # then
        with self.assertRaisesRegex(Exception, 'type_of_composition must be of type CompositionType'):
            classifier_data.validate_type_of_composition()

    def test_cross_validate_bagging_generate_all_permutations(self):
        # given
        generate_all_permutations = True
        bagging = True
        classifier_data = ClassifierData(generate_all_permutations = generate_all_permutations,
                                         bagging = bagging)
        # when
        classifier_data.cross_validate()
        # then
        self.assertFalse(classifier_data.generate_all_permutations)


if __name__ == '__main__':
    unittest.main()
