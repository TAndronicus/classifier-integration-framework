import numpy as np
import matplotlib.pyplot as plt
import MyLibrary

type_of_classifier = MyLibrary.ClfType.LINEAR
are_samples_generated = True
number_of_samples_if_generated = 10000
number_of_dataset_if_not_generated = 0
plot_mesh_step_size = .2
number_of_space_parts = 5
number_of_classifiers = 3
number_of_best_classifiers = number_of_classifiers - 1
draw_color_plot = False
write_computed_scores = False

clfs = MyLibrary.initialize_classifiers(number_of_classifiers, type_of_classifier)

X, y = MyLibrary.prepare_raw_data(are_samples_generated, number_of_samples_if_generated, number_of_dataset_if_not_generated)

X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test = MyLibrary.split_sorted_samples(X, y, number_of_classifiers, number_of_space_parts)

xx, yy, x_min_plot, x_max_plot = MyLibrary.get_plot_data(X, plot_mesh_step_size)
number_of_subplots = MyLibrary.determine_number_of_subplots(draw_color_plot, number_of_classifiers)

clfs, coefficients = MyLibrary.train_classifiers(clfs, X_whole_train, y_whole_train, type_of_classifier, number_of_subplots, X, plot_mesh_step_size, draw_color_plot)

scores = MyLibrary.test_classifiers(clfs, number_of_space_parts, X_validation, y_validation, X, coefficients, write_computed_scores)

# Prepare plot of composite
ax = plt.subplot(1, number_of_subplots, number_of_subplots)
ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test)

# Preparing composite classifier
scores = MyLibrary.prepare_composite_classifier(X_test, y_test, X, number_of_space_parts, number_of_classifiers, number_of_best_classifiers, coefficients, scores, plot_mesh_step_size, ax)

# Print resilts
i = 1
for row in scores:
    print('Classifier ' + str(i))
    print(row)
    i += 1
plt.show()