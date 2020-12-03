from treelib import Tree
from alternat.generation.exceptions import OCRClusteringException


class ClusterTree(object):
    """Alternat clustering implementation class.

    :param object: [description]
    :type object: [type]
    :return: [description]
    :rtype: [type]
    """

    # the bounding boxes should fall within threshold * 100 of width or height
    OVERLAP_THRESHOLD = 0.95

    def __init__(self):
        self.tree = Tree()
        self.root = "root"
        self.tree.create_node(self.root, self.root, data=[])

    def add_node(self, parent_name: str, node_name: str, data):
        """Adds a node in the tree (uses treelib).

        :param parent_name: Tag of the parent in the tree.
        :type parent_name: str
        :param node_name: Tag of the node to be added in the tree.
        :type node_name: str
        :param data: Data to be stored in the node.
        :type data: [type]
        """
        self.tree.create_node(node_name.upper(), node_name, data=data, parent=parent_name)

    def _find_next_overlapping_line_top(self, lines_sorted_top, current_line, line_with_max_bottom):
        """Find the next overlapping element based on top values of line.

        :param lines_sorted_top: Sorted list of lines based on their top values.
        :type lines_sorted_top: [type]
        :param current_line: Current line object.
        :type current_line: [type]
        :param line_with_max_bottom: Line with max bottom value.
        :type line_with_max_bottom: [type]
        :return: [description]
        :rtype: [type]
        """
        starting_index = lines_sorted_top.index(current_line)
        remaining_lines = lines_sorted_top[starting_index + 1:]

        max_line_height = line_with_max_bottom["bottom"] - line_with_max_bottom["top"]
        threshold_height = max_line_height * self.OVERLAP_THRESHOLD

        overlapping_lines = list(filter(lambda line: (line["top"] >= current_line["top"]) and
                                                     (line["top"] < (line_with_max_bottom["top"] + threshold_height)),
                                        remaining_lines))

        if len(overlapping_lines) > 0:

            next_overlapping_line = overlapping_lines[0]
            new_line_with_max_bottom = line_with_max_bottom

            if next_overlapping_line["bottom"] > line_with_max_bottom["bottom"]:
                new_line_with_max_bottom = next_overlapping_line

            return [next_overlapping_line, new_line_with_max_bottom]
        else:
            return [None, line_with_max_bottom]

    def _find_next_overlapping_line_left(self, lines_sorted_left, current_line, line_with_max_right):
        """Find the next overlapping element based on left values of line.

        :param lines_sorted_left: Sorted list of lines based on their left values.
        :type lines_sorted_left: [type]
        :param current_line: Current line object.
        :type current_line: [type]
        :param line_with_max_right: Line with max right value.
        :type line_with_max_right: [type]
        :return: [description]
        :rtype: [type]
        """
        starting_index = lines_sorted_left.index(current_line)
        remaining_lines = lines_sorted_left[starting_index + 1:]

        max_line_right = line_with_max_right["right"] - line_with_max_right["left"]
        threshold_width = max_line_right * self.OVERLAP_THRESHOLD

        overlapping_lines = list(filter(lambda line: (line["left"] >= current_line["left"]) and
                                                     (line["left"] < (line_with_max_right["left"] + threshold_width)),
                                        remaining_lines))

        if len(overlapping_lines) > 0:

            next_overlapping_line = overlapping_lines[0]
            new_line_with_max_right = line_with_max_right

            if next_overlapping_line["right"] > line_with_max_right["right"]:
                new_line_with_max_right = next_overlapping_line

            return [next_overlapping_line, new_line_with_max_right]
        else:
            return [None, line_with_max_right]

    def _create_row_clusters(self, data: list):
        """Create row clusters based on the transformed line data.

        :param data: Transformed line data with bounding box info in the form {top: value, right: value, bottom: value, left: value}.
        :type data: list
        :return: [description]
        :rtype: [type]
        """
        clusters = []
        cluster_number = 0

        line_index = 0

        sorted_top = sorted(data, key=lambda line: line["top"])

        while line_index < len(data):
            cluster = []
            cluster_number += 1
            line_with_max_bottom = None

            next_line_within_height = sorted_top[line_index]
            line_with_max_bottom = sorted_top[line_index]

            while next_line_within_height is not None:
                cluster.append(next_line_within_height)
                current_line = next_line_within_height

                overlapping_line_data = self._find_next_overlapping_line_top(sorted_top,
                                                                             current_line,
                                                                             line_with_max_bottom)

                next_line_within_height = overlapping_line_data[0]
                line_with_max_bottom = overlapping_line_data[1]

            sorted_cluster = sorted(cluster, key=lambda line: line["left"])

            clusters.append(sorted_cluster)
            line_index += len(cluster)

        return clusters

    def _create_column_clusters(self, data: list):
        """Creates column clusters in the transformed line data.

        :param data: Transformed line data with bounding box info in the form {top: value, right: value, bottom: value, left: value}.
        :type data: list
        :return: [description]
        :rtype: [type]
        """
        clusters = []
        cluster_number = 0

        line_index = 0

        sorted_left = sorted(data, key=lambda line: line["left"])

        while line_index < len(data):
            cluster = []
            cluster_number += 1
            line_with_max_right = None

            next_line_within_width = sorted_left[line_index]
            line_with_max_right = sorted_left[line_index]

            while next_line_within_width is not None:
                cluster.append(next_line_within_width)
                current_line = next_line_within_width

                overlapping_line_data = self._find_next_overlapping_line_left(sorted_left,
                                                                              current_line,
                                                                              line_with_max_right)

                next_line_within_width = overlapping_line_data[0]
                line_with_max_right = overlapping_line_data[1]

            sorted_cluster = sorted(cluster, key=lambda line: line["top"])

            clusters.append(sorted_cluster)
            line_index += len(cluster)

        return clusters

    def _combine_nodes(self, data: list):
        """Combine nodes which are part of the cluster because they are closed to each other

        :param data: Transformed line data with bounding box info in the form {top: value, right: value, bottom: value, left: value}.
        :type data: list
        :return: [description]
        :rtype: [type]
        """
        node_text = ""

        sorted_top = sorted(data, key=lambda line: line["top"])
        for line_data in sorted_top:
            node_text += line_data["text"] + " "

        return {
            "left": min([line_data["left"] for line_data in sorted_top]),
            "top": min([line_data["top"] for line_data in sorted_top]),
            "right": max([line_data["right"] for line_data in sorted_top]),
            "bottom": max([line_data["bottom"] for line_data in sorted_top]),
            "text": node_text
        }

    def _create_tree(self, cluster_type: str, lines_data: list, parent_name: str, parent_cluster_type: str = None):
        """Recursive method to cluster lines data into columns and rows clusters. The recursion return when the leaf
        node is encountered.

        :param cluster_type: The type cluster to make (ROW / COL).
        :type cluster_type: str
        :param lines_data: Transformed line data with bounding box info in the form {top: value, right: value, bottom: value, left: value}.
        :type lines_data: list
        :param parent_name: Name / Tag of the parent node.
        :type parent_name: str
        :param parent_cluster_type: The type of cluster for parent, defaults to None (ROW)
        :type parent_cluster_type: str, optional
        """

        row_index = 0
        column_index = 0

        if cluster_type == "ROW":

            if len(lines_data) > 1:

                cluster_data = self._create_row_clusters(lines_data)

                if parent_cluster_type == "COL" and len(cluster_data) == 1:
                    # add a leaf node with combined data
                    node = self._combine_nodes(cluster_data[0])

                    node_name = parent_name + "L"
                    self.add_node(parent_name, node_name, {
                        "children": [],
                        "val": node
                    })
                else:
                    for data in cluster_data:
                        row_index += 1
                        node_name = parent_name + "R" + str(row_index)
                        self.add_node(parent_name, node_name, {
                            "children": data
                        })

                        # print("Row cluster : ", row_index, data, node_name)

                        self._create_tree("COL", data, node_name, "ROW")
            else:

                if len(lines_data) == 1:
                    node_name = parent_name + "L"
                    self.add_node(parent_name, node_name, {
                        "children": [],
                        "val": lines_data[0]
                    })

        if cluster_type == "COL":
            if len(lines_data) > 1:

                cluster_data = self._create_column_clusters(lines_data)

                if parent_cluster_type == "ROW" and len(cluster_data) == 1:
                    # add a leaf node with combined data
                    node = self._combine_nodes(cluster_data[0])

                    node_name = parent_name + "L"
                    self.add_node(parent_name, node_name, {
                        "children": [],
                        "val": node
                    })

                else:
                    for data in cluster_data:
                        column_index += 1
                        node_name = parent_name + "C" + str(column_index)
                        self.add_node(parent_name, node_name, {
                            "children": data
                        })

                        # print("Column cluster : ", column_index, data, node_name)

                        self._create_tree("ROW", data, node_name, "COL")
            else:
                if len(lines_data) == 1:
                    node_name = parent_name + "L"
                    self.add_node(parent_name, node_name, {
                        "children": [],
                        "val": lines_data[0]
                    })

    @staticmethod
    def _update_data(lines_data: list):
        """Transforms ocr bounding box data from rule engine of form 
        [{x: left, y: top}, {x: right, y: top}, {x: right, y: bottom}, {x: left, y: bototm}] to [{top: value, right: value, left: value, bottom: value}]
        :param lines_data: OCR data after passing from rule engine.
        :type lines_data: list
        :return: [description]
        :rtype: [type]
        """
        updated_lines_data = []
        for line in lines_data:

            left = min([bb["x"] for bb in line["boundingBox"]])
            top = min([bb["y"] for bb in line["boundingBox"]])
            right = max([bb["x"] for bb in line["boundingBox"]])
            bottom = max([bb["y"] for bb in line["boundingBox"]])
            new_data = {
                "top": top,
                "left": left,
                "right": right,
                "bottom": bottom,
                "confidence": line["confidence"],
                "text": line["text"]
            }

            updated_lines_data.append(new_data)

        return updated_lines_data

    def _generate_ocr_text_from_tree(self):
        """Generates OCR text from the tree. Does the Depth-first traversal
        to find leaf nodes and appends the text to generate final OCR text.

        :return: [description]
        :rtype: [type]
        """
        ocr_text = ""
        for node in self.tree.expand_tree(mode=Tree.DEPTH):
            node_id = self.tree[node].tag
            last_char_node_id = node_id[len(node_id) - 1]

            # only if the node is the leaf node
            if last_char_node_id == "L":
                # print("Running for node ", node_id, self.tree[node].data["val"]["text"])
                ocr_text += self.tree[node].data["val"]["text"] + " "
        return ocr_text

    def generate_data(self, lines_data):
        """Main handler for alternat clustering implementation. The method
        internally creates clusters, save it on the tree and generates the final
        OCR text from it.

        :param lines_data: OCR data after passing from rule engine.
        :type lines_data: [type]
        :return: [description]
        :rtype: [type]
        """
        modified_lines_data = self._update_data(lines_data)
        #
        # print(" line data : ", modified_lines_data)
        cluster_type = "ROW"
        parent_name = self.root

        # adding a general exception to catch infinite loop error
        try:
            self._create_tree(cluster_type, modified_lines_data, parent_name)
        except:
            OCRClusteringException()
            return ""

        ocr_data = self._generate_ocr_text_from_tree()
        return ocr_data










