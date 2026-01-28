from strategytester5 import datetime, ORDER_TYPE_MAP, ORDER_STATE_MAP, DEAL_ENTRY_MAP, DEAL_TYPE_MAP
from strategytester5.stats import TesterStats

def html_report_template() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Strategy Tester Report</title>
    
        <!-- Bootstrap 5 -->
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
            rel="stylesheet"
        >
    
        <style>
            :root {
                --bg: #ffffff;
                --border: #dee2e6;
                --header-bg: #f3f4f6;
                --text: #212529;
                --muted: #6c757d;
            }
    
            body {
                background: var(--bg);
                font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
                font-size: 11px;
                color: var(--text);
                line-height: 1.35;
            }
    
            /* Page width */
            .page-wrapper {
                margin: 24px 10%;
            }
    
            h4 {
                font-size: 13px;
                font-weight: 600;
                text-align: center;
                margin: 22px 0 10px;
            }
    
            .muted {
                color: var(--muted);
                font-size: 10px;
            }
    
            /* Sections are logical only – no visual boxes */
            .section {
                margin-bottom: 18px;
            }
    
            /* Unified report table style */
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 10px;
            }
    
            th, td {
                padding: 4px 6px;
                border: 1px solid var(--border);
                text-align: center;
                vertical-align: middle;
                white-space: nowrap;
            }
    
            th {
                background: var(--header-bg);
                font-weight: 600;
            }
    
            td.number {
                text-align: right;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            }
    
            /* Stats table slightly larger */
            .report-table th,
            .report-table td {
                font-size: 11px;
                padding: 6px 8px;
            }
    
            /* Curve */
            .curve-wrapper {
                display: flex;
                justify-content: center;
                margin: 12px 0 16px;
            }
    
            .curve-img {
                max-width: 60%;
            }
    
            /* Clean Bootstrap interference */
            .table-striped > tbody > tr:nth-of-type(odd) {
                background-color: #fafafa;
            }
    
            .table-responsive {
                overflow-x: auto;
            }
            
            /* ---------- Responsive Scaling ---------- */
    
            /* Page width adapts */
            .page-wrapper {
                margin: clamp(12px, 20vw, 20%);
            }
    
            /* Global font scales with viewport */
            body {
                font-size: clamp(9px, 0.75vw, 11px);
            }
    
            /* Headers scale gently */
            h4 {
                font-size: clamp(11px, 1vw, 13px);
            }
    
            /* Table font & spacing scale */
            table {
                font-size: clamp(8px, 0.7vw, 10px);
            }
    
            th, td {
                padding: clamp(2px, 0.4vw, 6px);
            }
    
            /* Stats table slightly larger */
            .report-table th,
            .report-table td {
                font-size: clamp(9px, 0.8vw, 11px);
            }
    
            /* Curve responsiveness */
            .curve-img {
                max-width: 100%;
                width: clamp(280px, 60vw, 900px);
                height: auto;
            }
    
            /* Allow horizontal scroll ONLY if needed */
            .table-responsive {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }
    
            /* Reduce whitespace on small screens */
            @media (max-width: 900px) {
                h4 {
                    margin: 16px 0 8px;
                }
    
                .section {
                    margin-bottom: 12px;
                }
            }
    
            /* Extreme small screens (last resort) */
            @media (max-width: 600px) {
                .page-wrapper {
                    margin: 8px;
                }
    
                table {
                    font-size: 8px;
                }
    
                th, td {
                    padding: 2px 3px;
                }
            }
    
        </style>
    
    </head>
    <body>
    
    <div class="page-wrapper">
    
        <h4>Strategy Tester Report<br><span class="muted">Python Simulator</span></h4>
    
        <h4>Stats</h4>
        <div class="section">
            {{STATS_TABLE}}
        </div>
    
        <div class="section">
            <div class="curve-wrapper">
                {{CURVE_IMAGE}}
            </div>
        </div>
    
        <h4>Orders</h4>
        <div class="section table-responsive">
            <table class="table table-sm table-striped align-middle">
                <thead>
                    <tr>
                        <th>Open Time</th>
                        <th>Order</th>
                        <th>Symbol</th>
                        <th>Type</th>
                        <th class="number">Volume</th>
                        <th class="number">Price</th>
                        <th class="number">S / L</th>
                        <th class="number">T / P</th>
                        <th>Time</th>
                        <th>State</th>
                        <th>Comment</th>
                    </tr>
                </thead>
                <tbody>
                    {{ORDER_ROWS}}
                </tbody>
            </table>
        </div>
    
        <h4>Deals</h4>
        <div class="section table-responsive">
            <table class="table table-sm table-striped align-middle">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Deal</th>
                        <th>Symbol</th>
                        <th>Type</th>
                        <th>Entry</th>
                        <th class="number">Volume</th>
                        <th class="number">Price</th>
                        <th class="number">Commission</th>
                        <th class="number">Swap</th>
                        <th class="number">Profit</th>
                        <th>Comment</th>
                        <th class="number">Balance</th>
                    </tr>
                </thead>
                <tbody>
                    {{DEAL_ROWS}}
                </tbody>
            </table>
        </div>
    
    </div>
    
    </body>
    </html>
    
    """

def render_order_rows(orders):

    rows = []

    for o in orders:
        rows.append(f"""
        <tr>
            <td>{datetime.fromtimestamp(o.time_setup)}</td>
            <td>{o.ticket}</td>
            <td>{o.symbol}</td>
            <td>{ORDER_TYPE_MAP.get(o.type, o.type)}</td>
            <td class="text-end">{o.volume_initial:.2f} / {o.volume_current:.2f}</td>
            <td class="text-end">{o.price_open:.5f}</td>
            <td class="text-end">{"" if o.sl == 0 else f"{o.sl:.5f}"}</td>
            <td class="text-end">{"" if o.tp == 0 else f"{o.tp:.5f}"}</td>
            <td>{datetime.fromtimestamp(o.time_done) if o.time_done else ""}</td>
            <td>{ORDER_STATE_MAP.get(o.state, o.state)}</td>
            <td>{o.comment}</td>
        </tr>
        """)

    return "\n".join(rows)


def render_deal_rows(deals):
    rows = []

    for d in deals:
        rows.append(f"""
        <tr>
            <td>{datetime.fromtimestamp(d.time)}</td>
            <td>{d.ticket}</td>
            <td>{d.symbol}</td>
            <td>{DEAL_TYPE_MAP[d.type]}</td>
            <td>{DEAL_ENTRY_MAP[d.entry]}</td>
            <td class="text-end">{d.volume:.2f}</td>
            <td class="text-end">{d.price:.5f}</td>
            <td class="text-end">{d.commission:.2f}</td>
            <td class="text-end">{d.swap:.2f}</td>
            <td class="text-end">{d.profit:.2f}</td>
            <td>{d.comment}</td>
            <td>{round(d.balance, 2)}</td>
        </tr>
        """)

    return "\n".join(rows)

def render_stats_table(stats: TesterStats) -> str:

    return f"""
        <table class="report-table table-sm table-striped">
            <tbody>
                <tr>
                    <th>Initial Deposit</th><td class="number">{stats.initial_deposit}</td>
                    <th>Ticks</th><td class="number">{stats.ticks}</td>
                    <th>Symbols</th><td class="number">{stats.symbols}</td>
                </tr>
                <tr>
                    <th>Total Net Profit</th><td class="number">{stats.net_profit:.2f}</td>
                    <th>Balance Drawdown Absolute</th><td class="number">{stats.balance_drawdown_absolute:.2f}</td>
                    <th>Equity Drawdown Absolute</th><td class="number">{stats.equity_drawdown_absolute:.2f}</td>
                </tr>
                <tr>
                    <th>Gross Profit</th><td class="number">{stats.gross_profit:.2f}</td>
                    <th>Balance Drawdown Maximal</th><td class="number">{stats.balance_drawdown_maximal:.2f} ({(stats.balance_drawdown_maximal/100):.2f}%)</td>
                    <th>Equity Drawdown Maximal</th><td class="number">{stats.equity_drawdown_maximal:.2f} ({(stats.equity_drawdown_maximal/100):.2f}%)</td>
                </tr>
                <tr>
                    <th>Gross Loss</th><td class="number">{stats.gross_loss:.2f}</td>
                    <th>Balance Drawdown Relative</th><td class="number">{stats.balance_drawdown_relative:.2f}% ({(stats.balance_drawdown_relative*100):.2f})</td>
                    <th>Equity Drawdown Relative</th><td class="number">{stats.equity_drawdown_relative:.2f}% ({(stats.equity_drawdown_relative*100):.2f})</td>
                </tr>
                <tr>
                    <th>Profit Factor</th><td class="number">{stats.profit_factor:.2f}</td>
                    <th>Expected Payoff</th><td class="number">{stats.expected_payoff:.2f}</td>
                    <th>Margin Level</th><td class="number">{stats.margin_level:.2f}%</td>
                </tr>
                <tr>
                    <th>Recovery Factor</th><td class="number">{stats.recovery_factor:.2f}</td>
                    <th>Sharpe Ratio</th><td class="number">{stats.sharpe_ratio:.2f}</td>
                    <th>Z-Score</th><td class="number">{stats.z_score:.2f}</td>
                </tr>
                <tr>
                    <th>AHPR</th><td class="number">{stats.ahpr_factor:.4f} ({stats.ahpr_percent:.2f}%)</td>
                    <th>LR Correlation</th><td class="number">{stats.lr_correlation:.2f}</td>
                    <th>OnTester result</th><td class="number">{stats.on_tester_results}</td>
                </tr>
                <tr>
                    <th>GHPR</th><td class="number">{stats.ghpr_factor:.4f} ({stats.ghpr_percent:.2f}%)</td>
                    <th>LR Standard Error</th><td class="number">{stats.lr_standard_error:.2f}</td>
                    <td></td><td></td>
                </tr>
                <tr>
                    <th>Total Trades</th><td class="number">{stats.total_trades}</td>
                    <th>Short Trades (won %)</th><td class="number">{stats.short_trades_won} ({100 * stats.short_trades_won / max(stats.total_short_trades, 1):.2f}%)</td>
                    <th>Long Trades (won %)</th><td class="number">{stats.long_trades_won} ({100 * stats.long_trades_won / max(stats.total_long_trades, 1):.2f}%)</td>
                </tr>
                <tr>
                    <th>Total Deals</th><td class="number">{stats.total_deals}</td>
                    <th>Profit Trades (% of total)</th><td class="number">{stats.profit_trades} ({100 * stats.profit_trades / max(stats.total_trades, 1):.2f}%)</td>
                    <th>Loss Trades (% of total)</th><td class="number">{stats.loss_trades} ({100 * stats.loss_trades / max(stats.total_trades, 1):.2f}%)</td>
                </tr>
                <tr>
                    <th>Largest Profit Trade</th><td class="number">{stats.largest_profit_trade:.2f}</td>
                    <th>Largest Loss Trade</th><td class="number">{stats.largest_loss_trade:.2f}</td>
                    <td></td><td></td>
                </tr>
                <tr>
                    <th>Average Profit Trade</th><td class="number">{stats.average_profit_trade:.2f}</td>
                    <th>Average Loss Trade</th><td class="number">{stats.average_loss_trade:.2f}</td>
                    <td></td><td></td>
                </tr>
                <tr>
                    <th>Max Consecutive Wins ($)</th><td class="number">{stats.maximum_consecutive_wins_count} ({stats.maximum_consecutive_wins_money:.2f})</td>
                    <th>Max Consecutive Losses ($)</th><td class="number">{stats.maximum_consecutive_losses_count} ({stats.maximum_consecutive_losses_money:.2f})</td>
                    <td></td><td></td>
                </tr>
                <tr>
                    <th>Maximal Consecutive Profit (count)</th><td class="number">{stats.maximal_consecutive_profit_count} ({stats.maximal_consecutive_profit_money:.2f})</td>
                    <th>Maximal Consecutive Loss (count)</th><td class="number">{stats.maximal_consecutive_loss_count} ({stats.maximal_consecutive_loss_money:.2f})</td>
                    <td></td><td></td>
                </tr>
                <tr>
                    <th>Average Consecutive Wins</th><td class="number">{stats.average_consecutive_wins:.2f}</td>
                    <th>Average Consecutive Losses</th><td class="number">{stats.average_consecutive_losses:.2f}</td>
                    <td></td><td></td>
                </tr>
            </tbody>
        </table>
        """