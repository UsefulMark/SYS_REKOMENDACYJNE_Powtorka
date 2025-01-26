import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))


#%%

class RBM:
    def __init__(self, no_v, no_h):
        self.no_v = no_v
        self.no_h = no_h
        self.W = np.random.normal(0, 0.01,(no_v, no_h))
        self.bias_v = np.random.normal(0,1,no_v)*0.1
        self.bias_h = np.random.normal(0,1,no_h)*0.1

    def activate_hidden(self, v):
        prawdo = sigmoid(np.matmul(v, self.W) + self.bias_h)
        act = np.asarray(np.random.random(self.no_h) < prawdo, dtype=int)
        return act, prawdo

    def activate_visible(self, h):
        prawdo = sigmoid(np.matmul(h, self.W.T) + self.bias_v)
        act = np.asarray(np.random.random(self.no_v) < prawdo, dtype=int)
        return act, prawdo

    def CD(self, X, k=1):
        E_data = np.zeros((self.no_v, self.no_h))
        E_recon = np.zeros((self.no_v, self.no_h))

        E_bv_data = np.zeros((1, self.no_v))
        E_bv_recon = np.zeros((1, self.no_v))

        E_bh_data = np.zeros((1, self.no_h))
        E_bh_recon = np.zeros((1, self.no_h))

        for v in X:
            v = v.reshape((1, -1))

            h_hat, pr_h = self.activate_hidden(v)
            #temp = h_hat * pr_h
            temp = h_hat

            E_bh_data  +=  pr_h
            E_bv_data  += v
            #E_data     += np.matmul(v.T, h_hat)*pr_h
            E_data     += np.matmul(v.T, pr_h)
            for idk in range(k):
                v, pr_v =  self.activate_visible(h_hat)
                h_hat, pr_h = self.activate_hidden(v)

            E_recon    += np.matmul(v.T, pr_h)
            E_bh_recon += pr_h
            E_bv_recon += v
        E_data /= len(X)
        E_recon /= len(X)
        E_bh_recon /= len(X)
        E_bv_recon /= len(X)
        E_bh_data /= len(X)
        E_bv_data /= len(X)

        return E_data, E_recon, E_bv_data, E_bv_recon, E_bh_data, E_bh_recon

    def fit(self, X, epochs = 10, k=1, lr=0.01):
        for e in range(epochs):
            Ed, Er, bvd, bvr, bhd, bhr = self.CD(X, k)
            self.W -= lr*(Er - Ed)
            self.bias_h -= lr*(bhr - bhd).flatten()
            self.bias_v -= lr*(bvr - bvd).flatten()
            test = self.recreate_error(X)
            print("{}: {}, {}".format(e, test[0], test[1]))
        return True

    def recreate_error(self, X):
      res = []
      en = []
      for v in X:
        h, _ = self.activate_hidden(v)
        v_hat, _ = self.activate_visible(h)
        res.append(np.abs(v-v_hat))
        en.append(np.matmul(np.matmul(v, self.W), h) +  np.matmul(v, self.bias_v) + np.matmul(h, self.bias_h))
      res= np.array(res)
      en = np.array(en)
      return res.mean(), -en.mean()

#%%
from keras.datasets import mnist
(X, Y), (Xt, Yt) = mnist.load_data()
X = X.reshape((X.shape[0], 28*28))
X = np.asarray(X, dtype=float)
Xt = Xt.reshape((Xt.shape[0], 28*28))
Xt = np.asarray(Xt, dtype=float)
X /= 255
Xt /= 255
X[X > 0.5] = 1
X[X <= 0.5] = 0

#%%
import matplotlib.pyplot as plt
model = RBM(28*28, 100)
model.fit(X, 10, lr=0.01)


#%%
j = 3
k=0
for i in np.random.randint(0,len(X), j):
  plt.subplot(j, 2, k*2+1)
  x, _ = model.activate_hidden(X[i])
  x, _ = model.activate_visible(x)
  x = x.reshape((28, 28))
  plt.imshow(x)
  plt.xticks([])
  plt.yticks([])
  plt.subplot(j, 2, k*2+2)
  plt.imshow(X[i].reshape((28,28)))
  k += 1
  plt.xticks([])
  plt.yticks([])


#%%
#Jedyna zmiana względem tego wyżej, to wprowadzenie mini-batchów
class RBM_b:
    def __init__(self, no_v, no_h):
        self.no_v = no_v
        self.no_h = no_h
        self.W = np.random.normal(0, 0.01,(no_v, no_h))
        self.bias_v = np.random.normal(0,1,no_v)*0.1
        self.bias_h = np.random.normal(0,1,no_h)*0.1

    def activate_hidden(self, v):
        prawdo = sigmoid(np.matmul(v, self.W) + self.bias_h)
        act = np.asarray(np.random.random(self.no_h) < prawdo, dtype=int)
        return act, prawdo

    def activate_visible(self, h):
        prawdo = sigmoid(np.matmul(h, self.W.T) + self.bias_v)
        act = np.asarray(np.random.random(self.no_v) < prawdo, dtype=int)
        return act, prawdo

    def CD(self, X, k=1):
        E_data = np.zeros((self.no_v, self.no_h))
        E_recon = np.zeros((self.no_v, self.no_h))

        E_bv_data = np.zeros((1, self.no_v))
        E_bv_recon = np.zeros((1, self.no_v))

        E_bh_data = np.zeros((1, self.no_h))
        E_bh_recon = np.zeros((1, self.no_h))

        for v in X:
            v = v.reshape((1, -1))

            h_hat, pr_h = self.activate_hidden(v)
            #temp = h_hat * pr_h
            temp = h_hat

            E_bh_data  +=  pr_h
            E_bv_data  += v
            #E_data     += np.matmul(v.T, h_hat)*pr_h
            E_data     += np.matmul(v.T, pr_h)
            for idk in range(k):
                v, pr_v =  self.activate_visible(h_hat)
                h_hat, pr_h = self.activate_hidden(v)

            E_recon    += np.matmul(v.T, pr_h)
            E_bh_recon += pr_h
            E_bv_recon += v

        E_data /= len(X)
        E_recon /= len(X)

        E_bh_recon /= len(X)
        E_bv_recon /= len(X)

        E_bh_data /= len(X)
        E_bv_data /= len(X)

        return E_data, E_recon, E_bv_data, E_bv_recon, E_bh_data, E_bh_recon

    def fit(self, X, epochs = 10, bs = 10, k=1, lr=0.01):
        for e in range(epochs):
          n_baches = X.shape[0] / bs
          for b in range(int(n_baches)):
            if b < n_baches-1:
              data = X[ b*bs : (b+1)*bs]
            else:
              data = X[ b*bs : ]

            Ed, Er, bvd, bvr, bhd, bhr = self.CD(data, k)
            self.W -= lr*(Er - Ed)
            self.bias_h -= lr*(bhr - bhd).flatten()
            self.bias_v -= lr*(bvr - bvd).flatten()
          test = self.recreate_error(X)
          print("{}: {}, {}".format(e+1, test[0], test[1]))
        return True

    def recreate_error(self, X):
      res = []
      en = []
      for v in X:
        h, _ = self.activate_hidden(v)
        v_hat, _ = self.activate_visible(h)
        res.append(np.abs(v-v_hat))
        en.append(np.matmul(np.matmul(v, self.W), h) +  np.matmul(v, self.bias_v) + np.matmul(h, self.bias_h))
      res= np.array(res)
      en = np.array(en)
      return res.mean(), -en.mean()


#%%
model2 = RBM_b(28*28, 100)
model2.fit(X, 10, lr=0.01)
j = 3
k=0
for i in np.random.randint(0,len(X), j):
  plt.subplot(j, 2, k*2+1)
  x, _ = model2.activate_hidden(X[i])
  x, _ = model2.activate_visible(x)
  x = x.reshape((28, 28))
  plt.imshow(x)
  plt.xticks([])
  plt.yticks([])
  plt.subplot(j, 2, k*2+2)
  plt.imshow(X[i].reshape((28,28)))
  k += 1
  plt.xticks([])
  plt.yticks([])