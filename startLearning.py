from utilities.DataProvider import DataProvider
from utilities.Brain import Brain
import multiprocessing as mp
import tensorflow as tf

if __name__ == "__main__":
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    # q = mp.Queue(100)
    # p = mp.Process(target=DataProvider, args=(q,))
    # p.start()

    data = DataProvider().provide_all_data()

    brain = Brain()
    brain.train_model(data)