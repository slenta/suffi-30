import matplotlib.pyplot as plt

months = ["02/20", "03/20", "04/20", "05/20", "06/20", "07/20",
          "08/20", "09/20", "10/20", "11/20", "12/20", "01/21"]
pageviews = [13968, 14989, 16562, 17272, 12609, 10940, 13701, 11577, 12224, 13520, 13849, 14568]
visitors  = [6611, 7370, 7848, 7855, 6545, 5681, 5639, 5864, 6242, 7121, 6987, 6959]

plt.figure(figsize = (8, 4))
plt.plot(months, visitors, "^--", label = "Visitors")
plt.plot(pageviews, "o:", label = "Pageviews")
plt.grid(True)
plt.ylim(0, 20000)
plt.legend()

plt.show()