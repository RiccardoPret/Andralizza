import pandas
import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def test_k(X_train, X_test, y_train, y_test, k, iteration=10):
	accuracy=0
	for i in range(0, iteration):
		clf = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
		clf.fit(X_train, y_train)
		accuracy += clf.score(X_test, y_test)

	return accuracy/iteration

def test_best_k(max_k=15):
	avg_accuracies={}
	X, y = get_dataset("train_features.txt")
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	for k in range(2, max_k+1):
		avg_accuracies[k] = test_k(X_train, X_test, y_train, y_test, k)

	return avg_accuracies


def cross_validate_classifier(k, X, y, n_folds=10):
	metrics_lists = {"accuracy": [], "precision": [], "recall": [], "F-measure": []}
	metrics = {}
	kfolds_indices_sets = KFold(n_folds)

	# The for has n_folds iterations
	for train_indices, test_indices in kfolds_indices_sets.split(X):
		clf = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
		clf.fit(X[train_indices], y[train_indices])
		y_pred = clf.predict(X[test_indices])
		metrics_lists["accuracy"].append(accuracy_score(y[test_indices], y_pred))
		metrics_lists["precision"].append(precision_score(y[test_indices], y_pred))
		metrics_lists["recall"].append(recall_score(y[test_indices], y_pred))
		metrics_lists["F-measure"].append(f1_score(y[test_indices], y_pred))

	for key, value in metrics_lists.items():
		metrics[key] = np.mean(value)

	return metrics


def test_best_k_kfold_cross_validation(max_k=15, cv=10):
	avg_metrics = {}
	X, y = get_dataset("train_features.txt")
	for k in range(2, max_k+1):
		avg_metrics[k] = cross_validate_classifier(k, X, y, n_folds=cv)

	return avg_metrics


def get_dataset(file):
	# Get the dataset
	dataset = pandas.read_csv(file)

	# Split the features from the label
	X = np.array(dataset.drop(['label'], 1))
	y = np.array(dataset['label'])

	return X, y


def print_metrics():
	metrics_dict = {}
	with open("./logs/metrics.txt", 'r') as f:
		for line in f:
			k = line.split('\t')[0]
			metrics = line.split('\t')[1]
			temp = []
			for metric in metrics.split(','):
				temp.append(metric.split(':')[1][1:].split('}')[0])
			metrics_dict[k] = temp

	for k, values in sorted(metrics_dict.items()):
		with open("./logs/latex.txt", 'a') as f:
			s=k
			for v in values:
				#Only the first 5 digits after the comma
				s+=" & "+v[:7]
			s+=" \\\ \n\hline\n"
			f.write(s)
	print(metrics_dict)


def classify(dataset="train_features.txt"):
	X, y = get_dataset(dataset)

	for k in range(9, 10):
		clf = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
		clf.fit(X, y)
		t = time.process_time()
		clf.predict(X)
		print("K= "+str(k)+str(time.process_time() - t))


def conf_matrix(dataset="train_features.txt"):
	X, y = get_dataset(dataset)
	kfolds_indices_sets = KFold(10)
	su=[0, 0, 0, 0]
	# The for has n_folds iterations
	for train_indices, test_indices in kfolds_indices_sets.split(X):
		clf = KNeighborsClassifier(n_neighbors=8, n_jobs=-1)
		clf.fit(X[train_indices], y[train_indices])
		y_pred = clf.predict(X[test_indices])
		conf=[]
		for array in confusion_matrix(y[test_indices], y_pred):
			for element in array:
				conf.append(element)
		print(conf)
		for v in range(0,4):
			su[v]+=conf[v]

	for v in su:
		print(v/10)


if __name__ == '__main__':
	conf_matrix()
	'''
	results = test_best_k_kfold_cross_validation(max_k=15)
	with open("./logs/metrics.txt", 'w') as f:
		for k, metrics in results.items():
			f.write(str(k)+'\t'+str(metrics)+'\n')
	'''
	# print_metrics()
