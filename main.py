# Importing the required libraries
from skimage.segmentation import felzenszwalb
from skimage.color import label2rgb
from skimage.data import astronaut
import skimage
import matplotlib.pyplot as plt
from skimage import graph

plt.figure(figsize=(10,5))

image = skimage.io.imread('images/WIN_20240904_14_30_32_Pro.jpg')
plt.imshow(image)
plt.show()
# exit(0)

image = skimage.filters.gaussian(image, sigma=5)

# Sample Image of scikit-image package
# astronaut = astronaut()

# computing the Felzenszwalb's
# Segmentation with sigma = 5 and minimum
# size = 100
image_segments = felzenszwalb(image,
                                  scale = 2,
                                  sigma=5,
                                  min_size=100)
rag = graph.rag_mean_color(image, image_segments)

def merge_boundary(graph, src, dst):
    """Call back called before merging 2 nodes.

    In this case we don't need to do any computation here.
    """
    pass


def weight_boundary(graph, src, dst, n):
    """
    Handle merging of nodes of a region boundary region adjacency graph.

    This function computes the `"weight"` and the count `"count"`
    attributes of the edge between `n` and the node formed after
    merging `src` and `dst`.


    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the "weight" and "count" attributes to be
        assigned for the merged node.

    """
    default = {'weight': 0.0, 'count': 0}
    # print(graph[src])
    # print(src)
    # print(graph[src].get(n, default))
    count_src = 1 or graph[src].get(n, default)['count']
    count_dst = 1 or graph[dst].get(n, default)['count']

    weight_src = graph[src].get(n, default)['weight']
    weight_dst = graph[dst].get(n, default)['weight']
    # print(graph[src].get(dst))
    # count = count_src + count_dst
    return {
        # 'count': count,
        'weight': max(count_src * weight_src , count_dst * weight_dst), # TODO: 
    }
#  rag initialization weird
print(rag,rag.edges.data())

merged_segments = graph.merge_hierarchical(image_segments, rag, thresh=.24, rag_copy=False,
                                           in_place_merge=True,
                                           merge_func=merge_boundary,
                                           weight_func=weight_boundary)
print(merged_segments)
print(rag,rag.edges.data())

# Plotting the original image
plt.subplot(1,2,1)
plt.imshow(image)
plt.subplot(1,2,2)
plt.imshow(skimage.segmentation.mark_boundaries(image,merged_segments))
plt.show()
# manually merge stuff? idkk
# print(image_segments)