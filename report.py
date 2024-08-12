def generate_report(analysis_results) -> str:
    report_lines = []

    report_lines.append("Times when PM2.5 level went above 30:")
    for timestamp in analysis_results['above_threshold']:
        report_lines.append(timestamp)

    report_lines.append("\nDaily statistics:")
    for row in analysis_results['daily_stats']:
        report_lines.append(f"{row['date']} - Max: {row['max_pm25']}, Min: {row['min_pm25']}, Avg: {row['avg_pm25']:.2f}")

    return "\n".join(report_lines)