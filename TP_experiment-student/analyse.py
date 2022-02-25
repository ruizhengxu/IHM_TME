from codecs import ignore_errors
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg


def plot(df, save=False):
       
   df_copy = df.copy()
   # DATA PRE-PROCESSING
   # Remove row where target != click
   df_copy.drop(df_copy[(df_copy.target != df_copy.click)].index, inplace=True)
   # Remove useless rows
   df_copy.drop(["participant_id", "trial_id", "block_id", "target", "click"], axis=1, inplace=True)
   # Convert size to _x_ format
   df_copy["size"] = [str(np.sqrt(s).astype(int))+"x"+str(str(np.sqrt(s).astype(int))) \
                  for s in df_copy["size"]]
   # Sorting row by size and condition
   df_copy["temp"] = [len(c) for c in df_copy["condition"]]
   df_copy = df_copy.sort_values(by=["size", "temp"], ascending=True)
   df_copy.drop("temp", axis=1, inplace=True)
   
   sns.catplot(y="size", x="time", data=df_copy, kind="violin",
               palette="pastel")
   plt.xlabel("Time (seconds)")
   plt.ylabel("Size")
   if save: plt.savefig("logs/violin_size.png")
   plt.clf()
   
   sns.catplot(y="condition", x="time", data=df_copy, kind="violin",
               palette="pastel")
   plt.xlabel("Time (seconds)")
   plt.ylabel("Condition")
   if save: plt.savefig("logs/violin_cond.png")
   plt.clf()
   
   sns.catplot(x="size", y="time", hue="condition", data=df_copy, kind="point",
               capsize=0.05, errwidth=2, palette="pastel")
   plt.xlabel("Size")
   plt.ylabel("Time (seconds)")
   if save: plt.savefig("logs/line_size.png")
   plt.clf()
   
   sns.catplot(x="condition", y="time", hue="size", data=df_copy, kind="point",
               capsize=0.05, errwidth=2, palette="pastel")
   plt.xlabel("Condition")
   plt.ylabel("Time (seconds)")
   if save: plt.savefig("logs/line_cond.png")
   plt.clf()
   
   sns.catplot(x="size", y="time", hue="condition", data=df_copy, capsize=0.05, kind="bar",
               saturation=8, palette="pastel", errcolor="gray", errwidth=2)
   plt.xlabel("Size")
   plt.ylabel("Time (seconds)")
   if save: plt.savefig("logs/bar_size.png")
   plt.clf()
   
   sns.catplot(x="condition", y="time", hue="size", data=df_copy, capsize=0.05, kind="bar",
               saturation=8, palette="pastel", errcolor="gray", errwidth=2)
   plt.xlabel("Condition")
   plt.ylabel("Time (seconds)")
   if save: plt.savefig("logs/bar_cond.png")
   plt.clf()
   
def display_mean_std(df, show=False):
   mean_by_condition = df[["condition", "time"]]\
      .groupby(["condition"]).mean()
   mean_by_size = df[["size", "time"]]\
      .groupby(["size"]).mean()
   std_by_condition = df[["condition", "time"]]\
      .groupby(["condition"]).std()
   std_by_size = df[["size", "time"]]\
      .groupby(["size"]).std()
   
   condition = pd.concat([mean_by_condition, std_by_condition], axis=1)
   size = pd.concat([mean_by_size, std_by_size], axis=1)
   
   if show:
      print(condition.to_markdown())
      print(size.to_markdown())

if __name__=="__main__":
   # Load csv
   df = pd.read_csv("logs/results.csv")

   # Display the data with seaborn
   plot(df, save=True)
   
   # Display mean and std
   display_mean_std(df, show=False)
   
   # ANOVA test
   # the parameters are data=, dv=, wihtin=, subject=
   res = pg.rm_anova(data=df, dv="time", within=["size", "condition"], subject="participant_id")
   print(res.to_markdown())

   # Posthoc test (if necessary)
   # the parameters are data=, dv=, wihtin=, subject=
   # posthocs = pg.pairwise_ttests(data=df, dv="time", within=["condition", "size"], subject="participant_id")
   # print(posthocs.to_markdown())

