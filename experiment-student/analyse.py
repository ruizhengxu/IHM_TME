import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg


def plot(save=False):
   g = sns.FacetGrid(df, col="condition", hue="participant_id")
   g.map(sns.scatterplot, "size", "time", alpha=.7)
   g.add_legend()
   if save: g.savefig("1.png")
   plt.clf()
   
   sns.lineplot(x="size", y="time", hue="participant_id", ci="sd", data=df)
   if save: plt.savefig("2_size.png")
   plt.clf()
   sns.lineplot(x="condition", y="time", hue="participant_id", ci="sd", data=df)
   if save: plt.savefig("2_cond.png")
   plt.clf()
   
   sns.barplot(x="size", y="time", hue="participant_id", data=df, capsize=0.05, 
               saturation=8, palette="hls", errcolor="gray", errwidth=2, ci="sd")
   if save: plt.savefig("3_size.png")
   plt.clf()
   sns.barplot(x="condition", y="time", hue="participant_id", data=df, capsize=0.05, 
               saturation=8, palette="hls", errcolor="gray", errwidth=2, ci="sd")
   if save: plt.savefig("3_cond.png")
   plt.clf()

if __name__=="__main__":
   # Load csv
   df = pd.read_csv("logs/result.csv")
   # Data pre-processing
   df = df.drop(df[(df.target != df.click)].index) # Remove row where target != click
   # mean_by_condition = df[["participant_id", "condition", "time"]]\
   #    .groupby(["participant_id", "condition"]).mean()
   # mean_by_size = df[["participant_id", "size", "time"]]\
   #    .groupby(["participant_id", "size"]).mean()
   
   # Display the data with seaborn
   plot(save=False)
   
   # ANOVA test
   # the parameters are data=, dv=, wihtin=, subject=
   #res = pg.rm_anova( ... )
   #print(res)

   # Posthoc test (if necessary)
   # the parameters are data=, dv=, wihtin=, subject=
   #posthocs = pg.pairwise_ttests(dv='Temps_space', within=['Type', 'Nb_obj'], subject='Participant', data=df)
   #pg.print_table(posthocs)

