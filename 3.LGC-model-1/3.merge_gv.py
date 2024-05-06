import pandas as pd

df = pd.read_csv('tr1_tr2.sln', sep='\s+')

##tr1
df_tr1 = df[(df['type']==3) & (df['traitNo']==1)]
df_tr1_merge = pd.DataFrame(columns=['id', 'gv1', 'gv2', 'gv_merge'])
df_tr1_merge['id'] = df_tr1[df_tr1['term']=='1']['levels']
df_tr1_merge['gv1'] = df_tr1[df_tr1['term']=='1']['effect'].values
df_tr1_merge['gv2'] = df_tr1[df_tr1['term']=='2']['effect'].values
df_tr1_merge['gv_merge'] = df_tr1_merge['gv1'] + df_tr1_merge['gv2']
df_tr1_merge.to_csv('tr1.gv', index=None, sep='\t')

##tr2
df_tr2 = df[(df['type']==3) & (df['traitNo']==2)]
df_tr2_merge = pd.DataFrame(columns=['id', 'gv1', 'gv2', 'gv_merge'])
df_tr2_merge['id'] = df_tr2[df_tr2['term']=='1']['levels']
df_tr2_merge['gv1'] = df_tr2[df_tr2['term']=='1']['effect'].values
df_tr2_merge['gv2'] = df_tr2[df_tr2['term']=='2']['effect'].values
df_tr2_merge['gv_merge'] = df_tr2_merge['gv1'] + df_tr2_merge['gv2']
df_tr2_merge.to_csv('tr2.gv', index=None, sep='\t')