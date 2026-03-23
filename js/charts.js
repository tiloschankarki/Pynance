/* =============================================
   PYNANCE — charts.js
   Chart.js + amCharts initialization per page
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;

  if (page === 'dashboard') initDashboard();
  if (page === 'reports')   initReports();
  if (page === 'developer') initDeveloper();
});

/* ============================================
   DASHBOARD PAGE
   ============================================ */
function initDashboard() {

  /* -- Trend Chart (grouped bar) -- */
  const trendCtx = document.getElementById('trendChart');
  if (trendCtx) {
    new Chart(trendCtx, {
      type: 'bar',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [
          {
            label: 'New',
            data: [4200, 5100, 6800, 5400, 7200, 9100, 10500],
            backgroundColor: '#e05c5c',
            borderRadius: 4,
            barPercentage: 0.65,
          },
          {
            label: 'Renewals',
            data: [3100, 3800, 4200, 3600, 5100, 6400, 7800],
            backgroundColor: '#3dbcb8',
            borderRadius: 4,
            barPercentage: 0.65,
          },
          {
            label: 'Churns',
            data: [800, 950, 1100, 900, 1300, 1500, 1200],
            backgroundColor: '#1c2b3a',
            borderRadius: 4,
            barPercentage: 0.65,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { display: false },
            border: { display: false },
            ticks: { color: '#6b7280', font: { size: 11 } }
          },
          y: {
            grid: { color: '#f0f2f5' },
            border: { display: false, dash: [4,4] },
            ticks: {
              color: '#6b7280',
              font: { size: 11 },
              callback: v => '$' + (v >= 1000 ? (v/1000) + 'k' : v)
            }
          }
        }
      }
    });
  }

  /* -- Sales Donut Chart -- */
  const salesCtx = document.getElementById('salesChart');
  if (salesCtx) {
    new Chart(salesCtx, {
      type: 'doughnut',
      data: {
        labels: ['Basic Plan', 'Pro Plan', 'Advanced Plan', 'Enterprise Plan'],
        datasets: [{
          data: [140, 80, 90, 32],
          backgroundColor: ['#b2dfdb', '#3dbcb8', '#80cbc4', '#1c2b3a'],
          borderWidth: 0,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.parsed}`
            }
          }
        }
      }
    });
  }

  /* -- Support Tickets Tab Filter -- */
  const tabBtns = document.querySelectorAll('.ticket-tab-btn');
  const ticketItems = document.querySelectorAll('.ticket-item[data-status]');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      ticketItems.forEach(item => {
        const show = filter === 'all' || item.dataset.status === filter;
        item.style.display = show ? '' : 'none';
      });
    });
  });

  /* -- World Map (amCharts 5) -- */
  if (typeof am5 !== 'undefined' && document.getElementById('worldMap')) {
    const root = am5.Root.new('worldMap');
    root.setThemes([am5themes_Animated.new(root)]);

    const chart = root.container.children.push(
      am5map.MapChart.new(root, {
        panX: 'none',
        panY: 'none',
        wheelY: 'none',
        projection: am5map.geoNaturalEarth1()
      })
    );

    const polygonSeries = chart.series.push(
      am5map.MapPolygonSeries.new(root, {
        geoJSON: am5geodata_worldLow,
        exclude: ['AQ']
      })
    );

    polygonSeries.mapPolygons.template.setAll({
      fill: am5.color('#e0e0e0'),
      stroke: am5.color('#fff'),
      strokeWidth: 0.5,
      tooltipText: '{name}'
    });

    // Countries with "active customers"
    const activeCountries = [
      'US','CA','GB','DE','FR','AU','IN','BR','MX','ZA',
      'NG','EG','RU','JP','CN','KR','IT','ES','AR','CO',
      'CL','PL','SE','NO','FI','NL','BE','PH','ID','TH'
    ];

    polygonSeries.mapPolygons.template.adapters.add('fill', (fill, target) => {
      const id = target.dataItem && target.dataItem.get('id');
      if (activeCountries.includes(id)) return am5.color('#e05c5c');
      return fill;
    });
  }
}

/* ============================================
   REPORTS PAGE
   ============================================ */
function initReports() {

  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const colors = {
    primary: '#3dbcb8',
    danger: '#e05c5c',
    dark: '#1c2b3a',
    muted: '#b0bec5'
  };

  /* -- Monthly Revenue Line Chart -- */
  const revCtx = document.getElementById('revenueChart');
  if (revCtx) {
    new Chart(revCtx, {
      type: 'line',
      data: {
        labels: months,
        datasets: [{
          label: 'Revenue ($)',
          data: [8200, 9100, 10500, 9800, 11200, 12400, 13100, 12700, 14200, 15100, 14800, 16200],
          borderColor: colors.primary,
          backgroundColor: 'rgba(61,188,184,0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: colors.primary
        }]
      },
      options: chartLineOptions('Revenue ($)', v => '$' + (v >= 1000 ? (v/1000).toFixed(1) + 'k' : v))
    });
  }

  /* -- Customer Growth Bar Chart -- */
  const custCtx = document.getElementById('customerGrowthChart');
  if (custCtx) {
    new Chart(custCtx, {
      type: 'bar',
      data: {
        labels: months,
        datasets: [
          {
            label: 'New Customers',
            data: [310, 420, 510, 480, 590, 670, 720, 650, 810, 880, 840, 950],
            backgroundColor: colors.primary,
            borderRadius: 4,
          },
          {
            label: 'Churned',
            data: [40, 55, 62, 48, 70, 85, 78, 92, 68, 100, 88, 110],
            backgroundColor: colors.danger,
            borderRadius: 4,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { size: 11 }, padding: 14 }
          }
        },
        scales: {
          x: { grid: { display: false }, border: { display: false }, ticks: { color: '#6b7280', font: { size: 11 } } },
          y: { grid: { color: '#f0f2f5' }, border: { display: false }, ticks: { color: '#6b7280', font: { size: 11 } } }
        }
      }
    });
  }

  /* -- Churn Rate Trend -- */
  const churnCtx = document.getElementById('churnChart');
  if (churnCtx) {
    new Chart(churnCtx, {
      type: 'line',
      data: {
        labels: months,
        datasets: [{
          label: 'Churn Rate (%)',
          data: [2.8, 2.5, 2.6, 2.3, 2.7, 2.4, 2.1, 2.5, 2.2, 1.9, 2.0, 1.8],
          borderColor: colors.danger,
          backgroundColor: 'rgba(224,92,92,0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: colors.danger
        }]
      },
      options: chartLineOptions('Churn Rate (%)', v => v + '%')
    });
  }

  /* -- Plan Distribution Pie -- */
  const planCtx = document.getElementById('planDistChart');
  if (planCtx) {
    new Chart(planCtx, {
      type: 'doughnut',
      data: {
        labels: ['Basic', 'Pro', 'Advanced', 'Enterprise'],
        datasets: [{
          data: [5820, 4200, 4800, 1781],
          backgroundColor: ['#b2dfdb', colors.primary, '#80cbc4', colors.dark],
          borderWidth: 0,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: { position: 'right', labels: { font: { size: 11 }, padding: 12 } }
        }
      }
    });
  }
}

/* shared line chart options */
function chartLineOptions(label, tickCb) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false }
    },
    scales: {
      x: { grid: { display: false }, border: { display: false }, ticks: { color: '#6b7280', font: { size: 11 } } },
      y: {
        grid: { color: '#f0f2f5' },
        border: { display: false },
        ticks: { color: '#6b7280', font: { size: 11 }, callback: tickCb }
      }
    }
  };
}

/* ============================================
   DEVELOPER PAGE
   ============================================ */
function initDeveloper() {
  const apiCtx = document.getElementById('apiUsageChart');
  if (apiCtx) {
    const labels = [];
    const data = [];
    for (let i = 29; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      labels.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
      data.push(Math.floor(Math.random() * 3000) + 500);
    }

    new Chart(apiCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'API Requests',
          data,
          borderColor: '#3dbcb8',
          backgroundColor: 'rgba(61,188,184,0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 2,
          pointBackgroundColor: '#3dbcb8'
        }]
      },
      options: chartLineOptions('Requests', v => v.toLocaleString())
    });
  }

  /* -- Copy API Key -- */
  document.querySelectorAll('.copy-key-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.closest('.api-key-row').querySelector('.api-key-value').textContent.trim();
      navigator.clipboard.writeText(key).then(() => {
        showToast('API key copied to clipboard');
      }).catch(() => {
        showToast('Could not copy — please copy manually');
      });
    });
  });

  /* -- Revoke Key -- */
  document.querySelectorAll('.revoke-key-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (confirm('Are you sure you want to revoke this API key? This cannot be undone.')) {
        btn.closest('.api-key-row').style.opacity = '0.35';
        btn.textContent = 'Revoked';
        btn.disabled = true;
        showToast('API key revoked');
      }
    });
  });
}
