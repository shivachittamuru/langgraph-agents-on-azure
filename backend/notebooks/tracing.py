import os
import json
import logging
import contextlib
from typing import AsyncIterator, List
from prompty.tracer import Tracer, PromptyTracer
from opentelemetry import trace as oteltrace
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import Span, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
# from IPython.display import display, Markdown

_tracer = "prompty"

@contextlib.contextmanager
def trace_span(name: str):    
    tracer = oteltrace.get_tracer(_tracer)    
    with tracer.start_as_current_span(name) as span:        
        def verbose_trace(key, value):            
            if isinstance(value, dict):                
                for k, v in value.items():                  
                    verbose_trace(f"{key}.{k}", v)            
            else:                
                span.set_attribute(f"{key}", value)        
        yield verbose_trace
        
        

# Markdown Exporter
class MarkdownExporter:
    def __init__(self):
        self.collected_spans = []

    def export(self, spans: List[Span]):
        self.collected_spans.extend(spans)

    def format_report(self):
        if not self.collected_spans:
            print("### Trace Report\nNo spans recorded.")
            return

        print("### Trace Report\n")
        for span in self.collected_spans:
            self.format_span(span)
            
    def format_span(self, span:Span, level: int = 0):
        indent = "\t" * level
        duration = (span.end_time - span.start_time) / 1e9  # Convert nanoseconds to seconds
        print(f"{indent}- **Span Name**: `{span.name}`")
        print(f"{indent}  - **Execution Time**: `{duration:.2f} seconds`")
        print(f"{indent}  - **Attributes**: ")
        for key, value in span.attributes.items():
            print(f"{indent}    - **`{key}`**: `{value}`")
        if span.events:
            print(f"{indent}  - **Events**: ")
            for event in span.events:
                print(f"{indent}    - **Event Name**: `{event.name}`")
        


def init_tracing(local_tracing: bool = False):
    """
    Initialize tracing for the application
    If local_tracing is True, use the PromptyTracer
    If remote_tracing is True, use the OpenTelemetry tracer
    If remote_tracing is not specified, defaults to using the OpenTelemetry tracer only if local_tracing is False
    """

    if local_tracing:
        local_trace = PromptyTracer()
        Tracer.add("PromptyTracer", local_trace.tracer)
        # Tracer.add("ConsoleTracer", console_tracer)
        
        oteltrace.set_tracer_provider(TracerProvider())
        tracer = oteltrace.get_tracer(__name__)
        
        # Custom Markdown Exporter
        markdown_exporter = MarkdownExporter()
        span_processor = SimpleSpanProcessor(markdown_exporter)
        oteltrace.get_tracer_provider().add_span_processor(span_processor)
        
        # return oteltrace.get_tracer(_tracer)
        
    else:
        Tracer.add("OpenTelemetry", trace_span)

        azmon_logger = logging.getLogger("azure")
        azmon_logger.setLevel(logging.INFO)

        # oteltrace.set_tracer_provider(TracerProvider())

        # Configure Azure Monitor as the Exporter
        app_insights = os.getenv("APPINSIGHTS_CONNECTIONSTRING")

        # Add the Azure exporter to the tracer provider

        oteltrace.set_tracer_provider(TracerProvider(sampler=ParentBasedTraceIdRatio(1.0)))
        oteltrace.get_tracer_provider().add_span_processor(BatchSpanProcessor(AzureMonitorTraceExporter(connection_string=app_insights)))
        
        # # Markdown Exporter
        # markdown_exporter = MarkdownExporter()
        # oteltrace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(markdown_exporter))
        
        # oteltrace.get_tracer_provider().add_span_processor(
        #     SimpleSpanProcessor(trace_exporter)
        # )

        return oteltrace.get_tracer(_tracer)
    
    
# Utility for a root span
@contextlib.contextmanager
def root_span(tracer, name: str, **attributes):
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, value)
        yield span
        
        
tracer = init_tracing(False)
