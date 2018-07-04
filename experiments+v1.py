
# coding: utf-8

# In[6]:


get_ipython().magic('matplotlib inline')
import numpy as np
import pylab as pl
from matplotlib import collections  as mc


# In[113]:


lines = [[(0, 1), (1, 1)], [(2, 3), (3, 2.42)], [(1, 2), (1, 3)]]
c = np.array([(0.6, 0.2, 0.2, 1), (0, 1, 0, 1), (0, 0, 1, 1)])

lc = mc.LineCollection(lines, colors=c, linewidths=[5,2,4])
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)


# In[81]:


def binary_tree(n,seed,changes):
    lines = []
    lines.append(seed)
    if n>1:
        new_seed1 = [(seed[0][0]+seed[1][0]*np.cos(seed[1][1]),seed[0][1]+seed[1][0]*np.sin(seed[1][1])),(seed[1][0]*changes[0],seed[1][1]+changes[1])]
        new_seed2 = [(seed[0][0]+seed[1][0]*np.cos(seed[1][1]),seed[0][1]+seed[1][0]*np.sin(seed[1][1])),(seed[1][0]*changes[0],seed[1][1]-changes[1])]
        lines.extend(binary_tree(n-1,new_seed1,changes))
        lines.extend(binary_tree(n-1,new_seed2,changes))
    return lines
def transform_tree_to_coord(tree_lines):
    tree_transf = [[(pt[0][0],pt[0][1]),(pt[0][0]+pt[1][0]*np.cos(pt[1][1]),pt[0][1]+pt[1][0]*np.sin(pt[1][1]))] for pt in tree_lines]
    return(tree_transf)


# In[253]:


tree1_init = binary_tree(12, [(0,0),(1,np.pi/2)], [0.8,np.pi/16])
tree1 = transform_tree_to_coord(tree1_init)
widths1 = [10*pt[1][0] for pt in tree1_init]
lc = mc.LineCollection(tree1, linewidths=widths1)
fig, ax = pl.subplots(figsize=(20,20))
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)


# In[69]:


a = []
for i in range(100):
    a.append(np.random.choice([1,2,3],p=[0.1,0.1,0.8]))


# In[82]:


def random_tree(n,seed,changes):
    lines = []
    lines.append(seed)
    if n>1:
        branches = np.random.choice([2,3,4],p=[0.8,0.15,0.05])
        for b in range(branches):
            ang = np.random.uniform(low=-1,high=1)*changes[1]
            scale = np.random.uniform(low=0.8,high=1.2)*changes[0]
            new_seed = [(seed[0][0]+seed[1][0]*np.cos(seed[1][1]),seed[0][1]+seed[1][0]*np.sin(seed[1][1])),(seed[1][0]*scale,seed[1][1]+ang)]
            lines.extend(random_tree(n-1,new_seed,changes))
#         lines.extend(tree(n-1,new_seed2,changes))
    return lines


# In[233]:


def build_tree(n,seed,changes,width_mult):
    tree_init = random_tree(n,seed,changes)
    tree = transform_tree_to_coord(tree_init)
    widths = [width_mult*(pt[1][0]**1.3) for pt in tree_init]
    return (tree,widths)


# In[234]:


# tree2_init = random_tree(13, [(0,0),(1,np.pi/2)], [0.7,np.pi/24])
# tree2 = transform_tree_to_coord(tree2_init)
# widths = [10*pt[1][0] for pt in tree2_init]
# c = []
# for i in range(len(tree2)):
#     c.append((0,0,1,1))
tree2,widths2 = build_tree(15, [(0,0),(1,np.pi/2)], [0.7,np.pi/24],20)

lc = mc.LineCollection(tree2, colors=(0.6,0.2,0.3,1),linewidths=widths2)
fig, ax = pl.subplots(figsize=(16,16))
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
#colors: (0,0.7,0.3,1), (0,0.3,0.7,1),(0.3,0.3,0.7,1),(0,0.5,0.7,1),(0.6,0.1,0.2,1),(0.6,0.2,0.3,1)


# In[208]:


def build_forest(num_trees,forest_width,color_map,n,seed,changes,width_mult):
    trees = []
    widths = []
    colors = []
    for t in range(num_trees):
        xshift_t = np.random.uniform(low=-1*forest_width,high=forest_width)
        lscale_t = np.random.uniform(low=0.4,high=1)
        
        seed_t = [(seed[0][0] + xshift_t,seed[0][1]),(seed[1][0]*lscale_t,seed[1][1])]
        tree_t,width_t = build_tree(n,seed_t,changes,width_mult)
        color_choice = color_map[np.random.choice(range(len(color_map)))]
        colors_t = [color_choice] * len(width_t)
        
        trees.extend(tree_t)
        widths.extend(width_t)
        colors.extend(colors_t)
    return (trees,widths,colors)


# In[269]:


color_map = [(0,0.7,0.3,1),(0.3,0.3,0.7,1),(0,0.5,0.7,1),(0.6,0.2,0.3,1)]
w=4
trees,widths,colors = build_forest(70,w,color_map,13, [(0,0),(0.8,np.pi/2)], [0.7,np.pi/5],13)


# In[270]:


ct+=1
lc = mc.LineCollection(trees, colors=colors,linewidths=widths)
fig, ax = pl.subplots(figsize=(8*w,10))
ax.add_collection(lc)
ax.autoscale()
pl.savefig("D:/Personal/Projects/Recursive structures/Images/random forest "+ct+".png")
# ax.margins(0.1)

