from keras.models import load_model
from keras.utils import plot_model
import os
os.environ["PATH"] += os.pathsep + r"C:\\Program Files\\Graphviz\\bin"
os.environ["GRAPHVIZ_DOT"] = r"C:\\Program Files\\Graphviz\\bin\\dot.exe"
model = load_model('./model-nn/2_model_training_time_domain_tf.h5')
plot_model(model, to_file='model_summary.png', show_shapes=True, show_layer_names=True)