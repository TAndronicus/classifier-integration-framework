import matplotlib.pyplot as plt
import MyLibrary

type_of_classifier = MyLibrary.ClfType.LINEAR
are_samples_generated = False
number_of_samples_if_generated = 10000
number_of_dataset_if_not_generated = 1
switch_columns_while_loading = True
plot_mesh_step_size = .2
number_of_space_parts = 5
number_of_classifiers = 3
number_of_best_classifiers = number_of_classifiers - 1
draw_color_plot = False
write_computed_scores = True
show_plots = True

clfs = MyLibrary.initialize_classifiers(number_of_classifiers, type_of_classifier)

X, y = MyLibrary.prepare_raw_data(are_samples_generated, number_of_samples_if_generated,
                                  number_of_dataset_if_not_generated, number_of_classifiers,
                                  number_of_space_parts, switch_columns_while_loading)


X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test = \
    MyLibrary.split_sorted_samples(X, y, number_of_classifiers, number_of_space_parts)

xx, yy, x_min_plot, x_max_plot = MyLibrary.get_plot_data(X, plot_mesh_step_size)
number_of_subplots = MyLibrary.determine_number_of_subplots(draw_color_plot, number_of_classifiers)

number_of_permutations = 0

score_pro_permutation = []
while True:
    clfs, coefficients = MyLibrary.train_classifiers(clfs, X_whole_train, y_whole_train, type_of_classifier,
                                                     number_of_subplots, X, plot_mesh_step_size, draw_color_plot)

    scores, cumulated_scores = MyLibrary.test_classifiers(clfs, X_validation, y_validation, X, coefficients,
                                                          number_of_space_parts, write_computed_scores)

    confusion_matrices = MyLibrary.compute_confusion_matrix(clfs, X_test, y_test)

    scores, cumulated_score, conf_mat = \
        MyLibrary.prepare_composite_classifier(X_test, y_test, X, number_of_best_classifiers, coefficients, scores,
                                               number_of_subplots, number_of_space_parts, number_of_classifiers,
                                               plot_mesh_step_size)

    confusion_matrices.append(conf_mat)
    cumulated_scores.append(cumulated_score)
    score_pro_permutation.append(cumulated_scores)

    MyLibrary.print_results_with_conf_mats(scores, cumulated_scores, confusion_matrices)

    X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test = \
        MyLibrary.generate_permutation(X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test)
    number_of_permutations += 1

    if show_plots:
        plt.show()

    if number_of_permutations == number_of_classifiers + 2:
        break

MyLibrary.print_permutation_results(score_pro_permutation)
