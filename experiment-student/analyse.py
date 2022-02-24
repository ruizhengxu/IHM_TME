from codecs import ignore_errors
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg


def plot(save=False):
   
   sns.catplot(y="size", x="time", data=df, kind="boxen",
               palette="pastel")
   if save: plt.savefig("violin_size.png")
   plt.clf()
   
   sns.catplot(y="condition", x="time", data=df, kind="boxen",
               palette="pastel")
   if save: plt.savefig("violin_cond.png")
   plt.clf()
   
   # sns.catplot(x="size", y="time", hue="condition", data=df, kind="point",
   #             capsize=0.05, errwidth=2, palette="pastel")
   # if save: plt.savefig("line_size.png")
   # plt.clf()
   # sns.catplot(x="condition", y="time", hue="size", data=df, kind="point",
   #             capsize=0.05, errwidth=2, palette="pastel")
   # if save: plt.savefig("line_cond.png")
   # plt.clf()
   
   # sns.catplot(x="size", y="time", hue="condition", data=df, capsize=0.05, kind="bar",
   #             saturation=8, palette="pastel", errcolor="gray", errwidth=2)
   # if save: plt.savefig("bar_size.png")
   # plt.clf()
   # sns.catplot(x="condition", y="time", hue="size", data=df, capsize=0.05, kind="bar",
   #             saturation=8, palette="pastel", errcolor="gray", errwidth=2)
   # if save: plt.savefig("bar_cond.png")
   # plt.clf()

if __name__=="__main__":
   # Load csv
   df = pd.read_csv("logs/result.csv")
   
   # DATA PRE-PROCESSING
   # Remove row where target != click
   df.drop(df[(df.target != df.click)].index, inplace=True)
   # Remove useless rows
   df.drop(["participant_id", "trial_id", "block_id", "target", "click"], axis=1, inplace=True)
   # Convert size to _x_ format
   df["size"] = [str(np.sqrt(s).astype(int))+"x"+str(str(np.sqrt(s).astype(int))) \
                  for s in df["size"]]
   # Sorting row by size and condition
   df["temp"] = [len(c) for c in df["condition"]]
   df = df.sort_values(by=["size", "temp"], ascending=True)
   df.drop("temp", axis=1, inplace=True)
   # mean_by_condition = df[["participant_id", "condition", "time"]]\
   #    .groupby(["participant_id", "condition"]).mean()
   # mean_by_size = df[["participant_id", "size", "time"]]\
   #    .groupby(["participant_id", "size"]).mean()
   # print(df)
   # Display the data with seaborn
   plot(save=True)
   
   # ANOVA test
   # the parameters are data=, dv=, wihtin=, subject=
   #res = pg.rm_anova( ... )
   #print(res)

   # Posthoc test (if necessary)
   # the parameters are data=, dv=, wihtin=, subject=
   #posthocs = pg.pairwise_ttests(dv='Temps_space', within=['Type', 'Nb_obj'], subject='Participant', data=df)
   #pg.print_table(posthocs)

