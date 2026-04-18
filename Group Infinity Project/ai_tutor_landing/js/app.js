document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.getElementById('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(15, 23, 42, 0.9)';
            header.style.backdropFilter = 'blur(10px)';
            header.style.padding = '0.75rem 0';
            header.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
        } else {
            header.style.background = 'transparent';
            header.style.backdropFilter = 'none';
            header.style.padding = '1.5rem 0';
            header.style.borderBottom = 'none';
        }
    });

    // Chart.js Performance Chart
    const ctx = document.getElementById('performanceChart').getContext('2d');
    
    // Gradient for chart
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(34, 211, 238, 0.4)');
    gradient.addColorStop(1, 'rgba(34, 211, 238, 0)');

    const chartData = {
        math: [65, 72, 68, 85, 92],
        physics: [45, 55, 62, 70, 78],
        coding: [80, 85, 82, 90, 95]
    };

    let performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            datasets: [{
                label: 'Mastery Level (%)',
                data: chartData.math,
                borderColor: '#22d3ee',
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointBackgroundColor: '#22d3ee',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });

    // Subject Selector
    const subjectBtns = document.querySelectorAll('.subject-btn');
    subjectBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            subjectBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update chart data
            const subject = btn.dataset.subject;
            performanceChart.data.datasets[0].data = chartData[subject];
            
            // Change color based on subject
            if (subject === 'physics') {
                performanceChart.data.datasets[0].borderColor = '#a855f7';
                const pGradient = ctx.createLinearGradient(0, 0, 0, 400);
                pGradient.addColorStop(0, 'rgba(168, 85, 247, 0.4)');
                pGradient.addColorStop(1, 'rgba(168, 85, 247, 0)');
                performanceChart.data.datasets[0].backgroundColor = pGradient;
            } else if (subject === 'coding') {
                performanceChart.data.datasets[0].borderColor = '#6366f1';
                const cGradient = ctx.createLinearGradient(0, 0, 0, 400);
                cGradient.addColorStop(0, 'rgba(99, 102, 241, 0.4)');
                cGradient.addColorStop(1, 'rgba(99, 102, 241, 0)');
                performanceChart.data.datasets[0].backgroundColor = cGradient;
            } else {
                performanceChart.data.datasets[0].borderColor = '#22d3ee';
                performanceChart.data.datasets[0].backgroundColor = gradient;
            }

            performanceChart.update();
        });
    });

    // Reveal Animations on Scroll
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const heroRobot = document.getElementById('heroRobot');
    const themeIcon = themeToggle.querySelector('i');

    function updateTheme(isLight) {
        if (isLight) {
            body.classList.add('light-mode');
            heroRobot.src = 'assets/robot_light.png';
            themeIcon.setAttribute('data-lucide', 'sun');
        } else {
            body.classList.remove('light-mode');
            heroRobot.src = 'assets/robot_dark.png';
            themeIcon.setAttribute('data-lucide', 'moon');
        }
        lucide.createIcons(); // Refresh icons
    }

    themeToggle.addEventListener('click', () => {
        const isThemeLight = body.classList.toggle('light-mode');
        updateTheme(isThemeLight);
        localStorage.setItem('theme', isThemeLight ? 'light' : 'dark');
    });

    // Onboarding Logic
    const modal = document.getElementById('onboardingModal');
    const loginBtn = document.getElementById('loginBtn');
    const signUpBtn = document.getElementById('signUpBtn');
    const closeModal = document.getElementById('closeModal');
    const nextStep = document.getElementById('nextStep');
    const prevStep = document.getElementById('prevStep');
    const finishBtn = document.getElementById('finishOnboarding');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const streamSelect = document.getElementById('userStream');
    const subjectGrid = document.getElementById('subjectGrid');
    const userBtns = document.querySelector('.nav-btns');
    const userProfile = document.getElementById('userProfile');
    const welcomeMsg = document.getElementById('welcomeMsg');
    const logoutBtn = document.getElementById('logoutBtn');

    const streamMapping = {
        science: ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Computer Science'],
        commerce: ['Accountancy', 'Economics', 'Business Studies', 'Mathematics', 'Entrepreneurship'],
        arts: ['History', 'Geography', 'Political Science', 'Sociology', 'Psychology']
    };

    let selectedSubjects = [];

    const toggleModal = (show) => {
        modal.style.display = show ? 'flex' : 'none';
        if (show) {
            step1.classList.add('active');
            step2.classList.remove('active');
        }
    };

    [loginBtn, signUpBtn].forEach(btn => btn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleModal(true);
    }));

    closeModal.addEventListener('click', () => toggleModal(false));

    nextStep.addEventListener('click', () => {
        const name = document.getElementById('userName').value;
        const stream = streamSelect.value;
        
        if (!name || !stream) {
            alert('Please enter your name and select a stream.');
            return;
        }

        // Populate Subjects
        subjectGrid.innerHTML = '';
        streamMapping[stream].forEach(subject => {
            const item = document.createElement('div');
            item.className = 'subject-item';
            item.textContent = subject;
            item.onclick = () => {
                item.classList.toggle('selected');
                if (item.classList.contains('selected')) {
                    selectedSubjects.push(subject);
                } else {
                    selectedSubjects = selectedSubjects.filter(s => s !== subject);
                }
            };
            subjectGrid.appendChild(item);
        });

        step1.classList.remove('active');
        step2.classList.add('active');
    });

    prevStep.addEventListener('click', () => {
        step2.classList.remove('active');
        step1.classList.add('active');
    });

    finishBtn.addEventListener('click', () => {
        if (selectedSubjects.length === 0) {
            alert('Please select at least one subject.');
            return;
        }

        const userData = {
            name: document.getElementById('userName').value,
            class: document.getElementById('userClass').value,
            stream: streamSelect.value,
            subjects: selectedSubjects
        };

        localStorage.setItem('userSession', JSON.stringify(userData));
        toggleModal(false);
        checkSession();
    });

    const checkSession = () => {
        const session = JSON.parse(localStorage.getItem('userSession'));
        if (session) {
            userBtns.style.display = 'none';
            userProfile.style.display = 'flex';
            welcomeMsg.textContent = `Welcome, ${session.name}`;
            
            // Personalize Hero
            const streamName = session.stream.charAt(0).toUpperCase() + session.stream.slice(1);
            document.querySelector('.hero-title').innerHTML = `Master <span style="color: var(--accent);">${streamName}</span> with Your <span style="color: var(--accent);">Personal AI</span> Tutor`;
        } else {
            userBtns.style.display = 'flex';
            userProfile.style.display = 'none';
        }
    };

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('userSession');
        location.reload();
    });

    checkSession();

    // Initialize Animations
    document.querySelectorAll('.feature-card, .step, .preview-container').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        updateTheme(true);
    }
});
