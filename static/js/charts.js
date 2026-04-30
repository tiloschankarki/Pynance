/* =============================================
   PYNANCE — charts.js
   Chart.js init per page, driven by body.dataset.page
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;
  if (page === 'dashboard') initDashboard();
  if (page === 'visualize') initVisualize();
});

function readJSON(id, fallback) {
  const el = document.getElementById(id);
  if (!el) return fallback;
  try { return JSON.parse(el.textContent); } catch (_) { return fallback; }
}

/* ============================================
   DASHBOARD PAGE
   ============================================ */
function initDashboard() {
  const labels = readJSON('chart-labels', []);
  const income = readJSON('chart-income', []);
  const expenses = readJSON('chart-expenses', []);

  const totalIncome = income.reduce((a, b) => a + b, 0);
  const totalExpenses = expenses.reduce((a, b) => a + b, 0);

  /* -- Cash-flow grouped bar chart -- */
  const cashflowCtx = document.getElementById('cashflowChart');
  if (cashflowCtx && typeof Chart !== 'undefined') {
    new Chart(cashflowCtx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Income',
            data: income,
            backgroundColor: '#3dbcb8',
            borderRadius: 4,
            barPercentage: 0.65,
          },
          {
            label: 'Expenses',
            data: expenses,
            backgroundColor: '#e05c5c',
            borderRadius: 4,
            barPercentage: 0.65,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { display: false },
            border: { display: false },
            ticks: { color: '#6b7280', font: { size: 11 } },
          },
          y: {
            grid: { color: '#f0f2f5' },
            border: { display: false, dash: [4, 4] },
            ticks: {
              color: '#6b7280',
              font: { size: 11 },
              callback: (v) => '$' + (v >= 1000 ? (v / 1000).toFixed(1) + 'k' : v),
            },
          },
        },
      },
    });
  }

  /* -- Income vs Expense donut -- */
  const mixCtx = document.getElementById('mixChart');
  if (mixCtx && typeof Chart !== 'undefined') {
    new Chart(mixCtx, {
      type: 'doughnut',
      data: {
        labels: ['Income', 'Expenses'],
        datasets: [
          {
            data: [totalIncome, totalExpenses],
            backgroundColor: ['#3dbcb8', '#e05c5c'],
            borderWidth: 0,
            hoverOffset: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: $${ctx.parsed.toFixed(2)}`,
            },
          },
        },
      },
    });
  }
}
/* ============================================
   VISUALIZE PAGE
   ============================================ */
   function initVisualize() {
    const labels = readJSON('chart-labels', []);
    const income = readJSON('chart-income', []);
    const expenses = readJSON('chart-expenses', []);
    const net = readJSON('chart-net', []);
  
    const cashflowCtx = document.getElementById('cashFlowChart');
    if (cashflowCtx && typeof Chart !== 'undefined') {
      new Chart(cashflowCtx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Income',
              data: income,
              borderColor: '#3dbcb8',
              backgroundColor: 'rgba(61, 188, 184, 0.12)',
              tension: 0.35,
              fill: true,
            },
            {
              label: 'Expenses',
              data: expenses,
              borderColor: '#e05c5c',
              backgroundColor: 'rgba(224, 92, 92, 0.12)',
              tension: 0.35,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
          },
        },
      });
    }
  
    const netCtx = document.getElementById('netCashFlowChart');
    if (netCtx && typeof Chart !== 'undefined') {
      new Chart(netCtx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Net Cash Flow',
              data: net,
              borderColor: '#5b7cfa',
              backgroundColor: 'rgba(91, 124, 250, 0.12)',
              tension: 0.35,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
          },
        },
      });
    }
  }