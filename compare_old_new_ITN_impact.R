# compare_old_new_ITN_impact.R
#
# Caitlin Bever
# October 2020
#
# Evaluate impact of vector bug fix on ITN impact simulations from ABV framework

library(data.table)
library(ggplot2)

data.folder = "C:/Users/cbever/Dropbox (IDM)/Malaria Team Folder/projects/vector_biting_bug_fix/results/raw/prev/"

# Load in the burn-in and intervention files
mint.old = fread(paste0(data.folder,"MAP_20200924_test_vector_bug_Int_old.csv"))
mburn.old = fread(paste0(data.folder,"MAP_20200924_test_vector_bug_Burnin_old.csv"))

mint.new = fread(paste0(data.folder,"MAP_20200924_test_vector_bug_Int_new.csv"))
mburn.new = fread(paste0(data.folder,"MAP_20200924_test_vector_bug_Burnin_new.csv"))

# Merge the two tables based on site, see, and larval habitat
mall.old = merge(mint.old[day==1095],mburn.old[day==14235],
             by=c("Site_Name","Run_Number","x_Temporary_Larval_Habitat"))
mall.old[,sim:="old"]

mall.new = merge(mint.new[day==1095],mburn.new[day==14235],
                 by=c("Site_Name","Run_Number","x_Temporary_Larval_Habitat"))
mall.new[,sim:="new"]

mall = rbindlist(list(mall.old,mall.new))

# Add archetype column for the sake of plotting
mall[,arch:=paste0("Archetype ",Site_Name)]

mall.sub = mall[CM_Coverage==0 & IRS_Coverage==0,
                .(Site_Name,Run_Number,x_Temporary_Larval_Habitat,
                  arch,ITN_Coverage,final_prev,initial_prev,sim)]

mall.comp = dcast.data.table(mall.sub,
                             Site_Name+Run_Number+x_Temporary_Larval_Habitat+arch+ITN_Coverage ~ sim,
                             value.var=c("initial_prev","final_prev"))

# Plot the comparison of new and old prevalence
ggplot(mall.comp)+
  geom_smooth(aes(x=final_prev_old,y=final_prev_new-final_prev_old,
                  color=factor(ITN_Coverage)))+
  facet_wrap(~arch)+
  theme_bw()+
  ylab("delta prev (new - old)")+
  xlab("old final prevalence")+
  scale_color_discrete("ITN coverage")

ggplot(mall.comp)+
  geom_smooth(aes(x=final_prev_old,y=(final_prev_new-final_prev_old)/final_prev_old*100,
                  color=factor(ITN_Coverage)))+
  facet_wrap(~arch)+
  theme_bw()+
  ylab("percent change in prevalence")+
  xlab("old final prevalence")+
  scale_color_discrete("ITN coverage")+
  xlim(c(0.01,NA))
