from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime

console = Console()

def print_alert_rich(alert):
    console.print("\n"+"="*50, style="bold red")
    console.print("[!] ANOMALY DETECTED", style="bold red")
    console.print(f"    Time    : {alert['timestamp']}", style="red")
    console.print(f"    Source  : {alert['ip_source']}:{alert['port_source']}", style="red")
    console.print(f"    Target  : {alert['ip_destination']}:{alert['port_destination']}", style="red")
    console.print(f"    Packets : {alert['packet_count']}", style="red")
    console.print(f"    Bytes   : {alert['byte_count']}", style="red")
    console.print(f"    Duration: {alert['duration']}s", style="red")
    console.print(f"    Score   : {alert['anomaly_score']}", style="red")
    console.print("="*50+"\n", style="bold red")

def print_stats(active_flows, alert_count, sample_count):
    table= Table(
        title = f"PyNIDS -- Live Monitor | {datetime.now().strftime('%H:%M:%S')}",
        box = box.ROUNDED,
        style="cyan"
    )
    table.add_column("IP source", style="white")
    table.add_column("IP destination", style="white")
    table.add_column("Port destination", style="white")
    table.add_column("Packets", style="green")
    table.add_column("Bytes", style="green")
    table.add_column("Duration", style="yellow")

    for key, flow in list(active_flows.items())[:10]:
        duration = round(flow["last_time"]-flow["start_time"], 1)
        table.add_row(
            key[0],
            key[1],
            str(key[3]),
            str(flow["packet_count"]),
            str(flow["byte_count"]),
            f"{duration}s"
        )

    console.clear()
    console.print(table)
    console.print(f"[*] Active flows  : [cyan]{len(active_flows)}[/cyan]")
    console.print(f"[*] Total alerts  : [red]{alert_count}[/red]")
    console.print(f"[*] Training samples collected : [green]{sample_count}[/green]")
    