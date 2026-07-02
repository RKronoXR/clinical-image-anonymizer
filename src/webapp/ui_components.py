from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StateComponents:
    """Persistent Gradio states shared by the UI callbacks."""

    files_state: Any
    rectangle_state: Any
    batch_index_state: Any


@dataclass(frozen=True)
class UploadComponents:
    """Initial and secondary upload controls."""

    initial_upload_group: Any
    initial_batch_files: Any
    side_batch_files: Any


@dataclass(frozen=True)
class ExportComponents:
    """Export panel controls."""

    export_group: Any
    export_output_folder: Any
    export_name_prefix: Any
    export_randomize_order: Any
    export_button: Any


@dataclass(frozen=True)
class ViewerComponents:
    """Image viewer, navigation, and grid controls."""

    viewer_group: Any
    image_tabs: Any
    original_preview: Any
    overlay_preview: Any
    anonymized_preview: Any
    first_button: Any
    previous_button: Any
    batch_position: Any
    next_button: Any
    last_button: Any
    show_grid_checkbox: Any
    grid_size_input: Any
    grid_label_size_input: Any

    @property
    def preview_outputs(self) -> list[Any]:
        return [
            self.original_preview,
            self.overlay_preview,
            self.anonymized_preview,
        ]

    @property
    def navigation_outputs(self) -> list[Any]:
        return [
            self.original_preview,
            self.overlay_preview,
            self.anonymized_preview,
        ]


@dataclass(frozen=True)
class RectangleComponents:
    """Rectangle editor controls."""

    add_rectangle_button: Any
    delete_rectangle_button: Any
    rectangle_selector: Any
    x_input: Any
    y_input: Any
    width_input: Any
    height_input: Any
    update_rectangle_button: Any
    rectangles_json: Any

    @property
    def coordinate_inputs(self) -> list[Any]:
        return [
            self.x_input,
            self.y_input,
            self.width_input,
            self.height_input,
        ]


@dataclass(frozen=True)
class MetadataComponents:
    """Metadata display controls."""

    current_metadata_html: Any


@dataclass(frozen=True)
class UIComponents:
    """Top-level typed container for all Gradio components in the app."""

    state: StateComponents
    upload: UploadComponents
    export: ExportComponents
    viewer: ViewerComponents
    rectangle: RectangleComponents
    metadata: MetadataComponents

    @classmethod
    def from_component_maps(
        cls,
        *,
        state: StateComponents,
        initial_upload_components: dict[str, Any],
        export_components: dict[str, Any],
        workspace_components: dict[str, Any],
    ) -> UIComponents:
        """Create typed component groups from panel-builder dictionaries."""
        return cls(
            state=state,
            upload=UploadComponents(
                initial_upload_group=initial_upload_components["upload_group"],
                initial_batch_files=initial_upload_components["batch_files"],
                side_batch_files=workspace_components["side_batch_files"],
            ),
            export=ExportComponents(
                export_group=export_components["export_group"],
                export_output_folder=export_components["export_output_folder"],
                export_name_prefix=export_components["export_name_prefix"],
                export_randomize_order=export_components["export_randomize_order"],
                export_button=export_components["export_button"],
            ),
            viewer=ViewerComponents(
                viewer_group=workspace_components["viewer_group"],
                image_tabs=workspace_components["image_tabs"],
                original_preview=workspace_components["original_preview"],
                overlay_preview=workspace_components["overlay_preview"],
                anonymized_preview=workspace_components["anonymized_preview"],
                first_button=workspace_components["first_button"],
                previous_button=workspace_components["previous_button"],
                batch_position=workspace_components["batch_position"],
                next_button=workspace_components["next_button"],
                last_button=workspace_components["last_button"],
                show_grid_checkbox=workspace_components["show_grid_checkbox"],
                grid_size_input=workspace_components["grid_size_input"],
                grid_label_size_input=workspace_components["grid_label_size_input"],
            ),
            rectangle=RectangleComponents(
                add_rectangle_button=workspace_components["add_rectangle_button"],
                delete_rectangle_button=workspace_components["delete_rectangle_button"],
                rectangle_selector=workspace_components["rectangle_selector"],
                x_input=workspace_components["x_input"],
                y_input=workspace_components["y_input"],
                width_input=workspace_components["width_input"],
                height_input=workspace_components["height_input"],
                update_rectangle_button=workspace_components["update_rectangle_button"],
                rectangles_json=workspace_components["rectangles_json"],
            ),
            metadata=MetadataComponents(
                current_metadata_html=workspace_components["current_metadata_html"],
            ),
        )

    def public_component_map(self) -> dict[str, Any]:
        """Return the legacy public component map expected by callers."""
        return {
            "files_state": self.state.files_state,
            "initial_batch_files": self.upload.initial_batch_files,
            "side_batch_files": self.upload.side_batch_files,
            "export_group": self.export.export_group,
            "viewer_group": self.viewer.viewer_group,
            "batch_index_state": self.state.batch_index_state,
            "original_preview": self.viewer.original_preview,
            "overlay_preview": self.viewer.overlay_preview,
            "anonymized_preview": self.viewer.anonymized_preview,
            "batch_position": self.viewer.batch_position,
            "current_metadata_html": self.metadata.current_metadata_html,
            "rectangle_state": self.state.rectangle_state,
            "add_rectangle_button": self.rectangle.add_rectangle_button,
            "delete_rectangle_button": self.rectangle.delete_rectangle_button,
            "rectangle_selector": self.rectangle.rectangle_selector,
            "x_input": self.rectangle.x_input,
            "y_input": self.rectangle.y_input,
            "width_input": self.rectangle.width_input,
            "height_input": self.rectangle.height_input,
            "update_rectangle_button": self.rectangle.update_rectangle_button,
            "show_grid_checkbox": self.viewer.show_grid_checkbox,
            "grid_size_input": self.viewer.grid_size_input,
            "grid_label_size_input": self.viewer.grid_label_size_input,
            "rectangles_json": self.rectangle.rectangles_json,
            "export_output_folder": self.export.export_output_folder,
            "export_name_prefix": self.export.export_name_prefix,
            "export_randomize_order": self.export.export_randomize_order,
            "export_button": self.export.export_button,
        }
