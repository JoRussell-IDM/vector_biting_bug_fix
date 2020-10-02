library(data.table)
library(ggplot2)

# Load in the burn-in and intervention files
mint = fread("C:/Users/cbever/OneDrive - Institute for Disease Modeling/Malaria/MAP/itn_cube_amelia/MAP_20200924_test_vector_bug_Int_CBTEST.csv")
mburn = fread("C:/Users/cbever/OneDrive - Institute for Disease Modeling/Malaria/MAP/itn_cube_amelia/MAP_20200924_test_vector_bug_Burnin_CBTEST.csv")

# Only interested in the last timepoint from the burnin
mburn = mburn[day==14235]

# Merge the two tables based on site, see, and larval habitat
mall = merge(mint,mburn,by=c("Site_Name","Run_Number","x_Temporary_Larval_Habitat"))
mall = mall[day.x==1095] # Filter on impact after 3 years of interventions

# Add archetype column for the sake of plotting
mall[,arch:=paste0("Archetype ",Site_Name)]

# Initial vs final prev for no IRS only; point version
ggplot(mall[IRS_Coverage==0])+geom_point(aes(x=initial_prev,y=final_prev,color=factor(ITN_Coverage)))+
  facet_wrap(~arch)+
  theme_bw()+
  scale_color_discrete(name="ITN Coverage")

# Initial vs final prev for no IRS only; spline version
ggplot(mall[IRS_Coverage==0])+geom_smooth(aes(x=initial_prev,y=final_prev,color=factor(ITN_Coverage)))+
  facet_wrap(~arch)+
  theme_bw()+
  scale_color_discrete(name="ITN Coverage")