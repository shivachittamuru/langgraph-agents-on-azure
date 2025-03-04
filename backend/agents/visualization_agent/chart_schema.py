from pydantic import BaseModel, Field
from typing import Any, Literal, Optional, List, Dict, Union

# Font settings for text elements
class Font(BaseModel):
    family: Optional[str] = Field(None, description="Font family for the text.")
    size: Optional[int] = Field(None, description="Font size in pixels.")
    color: Optional[str] = Field(None, description="Font color in a valid CSS format.")

# Title settings for the chart and axis labels
class Title(BaseModel):
    text: str = Field(..., description="Title text for the chart or axis.")
    font: Optional[Font] = Field(None, description="Font configuration for the title.")
    x: Optional[float] = Field(None, description="X position of the title (0 to 1).")
    xanchor: Optional[str] = Field(None, description="Horizontal alignment of the title.")
    y: Optional[float] = Field(None, description="Y position of the title (0 to 1).")
    yanchor: Optional[str] = Field(None, description="Vertical alignment of the title.")
    pad: Optional[Dict[str, int]] = Field(None, description="Padding around the title.")

# Axis settings (used for both X and Y axes)
class Axis(BaseModel):
    title: Optional[Title] = Field(None, description="Title configuration for the axis.")
    showgrid: Optional[bool] = Field(None, description="Whether to show grid lines.")
    zeroline: Optional[bool] = Field(None, description="Whether to show the zero line.")
    showline: Optional[bool] = Field(None, description="Whether to draw the axis line.")
    showticklabels: Optional[bool] = Field(None, description="Whether to show tick labels.")
    tickmode: Optional[str] = Field(None, description="Tick mode ('auto', 'linear', 'array').")
    tickvals: Optional[List[float]] = Field(None, description="Custom tick values if tickmode is 'array'.")
    ticktext: Optional[List[str]] = Field(None, description="Custom tick labels corresponding to tickvals.")
    rangemode: Optional[str] = Field(None, description="Range mode ('normal', 'tozero', 'nonnegative').")
    autorange: Optional[bool] = Field(None, description="Whether to automatically scale the axis range.")
    range: Optional[List[float]] = Field(None, description="Manually specified axis range [min, max].")
    type: Optional[str] = Field(None, description="Type of axis ('linear', 'log', 'category', 'date').")
    tickangle: Optional[int] = Field(None, description="Angle of tick labels.")

# Legend configuration
class Legend(BaseModel):
    title: Optional[Title] = Field(None, description="Title configuration for the legend.")
    x: Optional[float] = Field(None, description="X position of the legend (0 to 1).")
    y: Optional[float] = Field(None, description="Y position of the legend (0 to 1).")
    orientation: Optional[str] = Field(None, description="Legend orientation ('h' for horizontal, 'v' for vertical).")
    font: Optional[Font] = Field(None, description="Font settings for legend labels.")
    bgcolor: Optional[str] = Field(None, description="Background color of the legend.")

# Margin settings
class Margin(BaseModel):
    l: Optional[int] = Field(None, description="Left margin (in pixels).")
    r: Optional[int] = Field(None, description="Right margin (in pixels).")
    t: Optional[int] = Field(None, description="Top margin (in pixels).")
    b: Optional[int] = Field(None, description="Bottom margin (in pixels).")
    pad: Optional[int] = Field(None, description="Padding between margin and plot.")

class ChartTrace(BaseModel):
    """Represents a single trace (data series) in the Plotly chart."""
    type: Literal["scatter", "bar", "line", "heatmap", "pie", "histogram", "box", "surface", "contour"] = Field(..., description="Type of the chart.")
    x: Optional[List[Any]] = Field(None, description="X-axis values (if applicable).")
    y: Optional[List[Any]] = Field(None, description="Y-axis values (if applicable).")
    z: Optional[List[Any]] = Field(None, description="Z-axis values for 3D charts.")
    values: Optional[List[Any]] = Field(None, description="Values for pie charts.")
    labels: Optional[List[str]] = Field(None, description="Labels for pie charts.")
    mode: Optional[str] = Field(None, description="Mode for scatter/line charts (e.g., 'lines', 'markers').")
    marker: Optional[Dict[str, Any]] = Field(None, description="Marker settings for styling.")
    line: Optional[Dict[str, Any]] = Field(None, description="Line settings for styling.")
    text: Optional[List[str]] = Field(None, description="Text annotations for data points.")
    name: Optional[str] = Field(None, description="Name of the data series.")

# Layout configuration
class Layout(BaseModel):
    title: Optional[Title] = Field(None, description="Title configuration for the chart.")
    xaxis: Optional[Axis] = Field(None, description="X-axis configuration.")
    yaxis: Optional[Axis] = Field(None, description="Y-axis configuration.")
    height: Optional[int] = Field(None, description="Height of the plot in pixels.")
    width: Optional[int] = Field(None, description="Width of the plot in pixels.")
    showlegend: Optional[bool] = Field(None, description="Whether to show the legend.")
    legend: Optional[Legend] = Field(None, description="Legend configuration.")
    margin: Optional[Margin] = Field(None, description="Margin configuration.")
    paper_bgcolor: Optional[str] = Field(None, description="Background color of the entire figure.")
    plot_bgcolor: Optional[str] = Field(None, description="Background color of the plotting area.")

# Main Plotly Chart Schema
class PlotlyChart(BaseModel):
    data: List[ChartTrace] = Field(..., description="List of data series (traces) for the chart.")
    layout: Layout = Field(..., description="Layout configuration for the plot.")