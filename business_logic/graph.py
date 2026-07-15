from os.path import join as join_path
from typing import Any

import networkx as nx
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

from business_logic.utils import fit_image_size
from pyui import UIGraph

from .constructor import WindowConstructor


class Graph(WindowConstructor):
    def __init__(self) -> None:
        super().__init__(UIGraph)

    def openEvent(self) -> None:
        super().openEvent()
        self.ui_window.comboBox_clan.addItems(self.workbook.sheetnames)
        self.grow_tree()
        self.ui_window.comboBox_clan.currentIndexChanged.connect(self.grow_tree)

    def closeEvent(self, *args: Any) -> None:
        self.ui_window.comboBox_clan.disconnect()
        self.ui_window.comboBox_clan.clear()
        super().closeEvent(*args)

    def grow_tree(self) -> None:
        clan_name = self.ui_window.comboBox_clan.currentText()
        worksheet = self.workbook[clan_name]

        # Clear the figure before creating a new one.
        self.ui_window.figure.clf()
        self.ui_window.figure.canvas.draw()

        if worksheet.max_column == 1 and worksheet.max_row == 1:
            return

        family_tree = nx.DiGraph()  # Directed graph.
        ax = self.ui_window.figure.add_subplot()
        id_to_name, id_to_image = {}, {}
        default_image = join_path("media_resources", "Default_avatar.png")

        # Iterate over rows and add edges to the graph.
        for row in worksheet.iter_rows(min_row=1, values_only=True):
            image_path = row[0]
            person_id, partner_id, father_id = row[1], row[2], row[3]
            mother_id, last_name, first_name = row[4], row[6], row[7]

            if not father_id and not mother_id and not partner_id:
                continue

            if father_id:
                family_tree.add_edge(father_id, person_id)
            if mother_id:
                family_tree.add_edge(mother_id, person_id)
            if partner_id:
                family_tree.add_edge(person_id, partner_id)

            id_to_image[person_id] = (
                join_path("avatars", image_path) if image_path else default_image
            )
            id_to_name[person_id] = f"{last_name} {first_name}"

        tree_layout = nx.nx_pydot.graphviz_layout(family_tree, prog="dot")
        tree_layout = {  # Flip the tree.
            node_id: (x, -y) for node_id, (x, y) in tree_layout.items()
        }

        for node_id, (x, y) in tree_layout.items():
            # Draw nodes with images.
            image = Image.open(id_to_image[node_id])
            image = image.resize(fit_image_size(image.size, 50))
            imagebox = OffsetImage(image)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            ax.add_artist(ab)

            ax.text(  # Adjusted the `y` coordinate to move text above the image.
                x,
                y + 20,
                id_to_name[node_id],
                ha="center",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1),
            )
        nx.draw_networkx_edges(
            family_tree,
            tree_layout,
            alpha=0.5,
            min_source_margin=30,
            min_target_margin=30,
        )
        ax.axis("off")
        self.ui_window.figure.canvas.draw()
        self.ui_window.figure.canvas.flush_events()
