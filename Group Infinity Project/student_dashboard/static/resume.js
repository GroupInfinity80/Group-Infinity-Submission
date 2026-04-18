/**
 * RESUME BUILDER LOGIC
 * Handles live preview, dynamic sections, and PDF export
 */

// Initial Data State
let resumeData = {
    name: "John Doe",
    title: "Software Engineering Student",
    email: "john@example.com",
    phone: "+1 234 567 890",
    location: "New York, USA",
    summary: "Dedicated and detail-oriented computer science student with a passion for building scalable web applications. Strong foundation in Python, JavaScript, and UI/UX design principles.",
    experience: [
        {
            role: "Full Stack Intern",
            company: "Tech Solutions Inc.",
            date: "June 2025 - Present",
            description: "Developed and maintained feature-rich web applications using React and Node.js. Optimized database queries resulting in 30% faster load times."
        }
    ],
    education: [
        {
            degree: "B.S. in Computer Science",
            school: "Global University of Technology",
            date: "2022 - 2026",
            description: "GPA: 3.9/4.0. Relevant Coursework: Data Structures, Algorithms, Web Development."
        }
    ],
    skills: "Python, JavaScript, React, Flask, SQL, UI/UX Design, Git"
};

// Initialize the builder
document.addEventListener('DOMContentLoaded', () => {
    loadInitialData();
    updatePreview();
    renderSidebarItems();
});

function loadInitialData() {
    document.getElementById('input-name').value = resumeData.name;
    document.getElementById('input-title').value = resumeData.title;
    document.getElementById('input-email').value = resumeData.email;
    document.getElementById('input-phone').value = resumeData.phone;
    document.getElementById('input-location').value = resumeData.location;
    document.getElementById('input-summary').value = resumeData.summary;
    document.getElementById('input-skills').value = resumeData.skills;
}

function updatePreview() {
    // Collect data from inputs
    resumeData.name = document.getElementById('input-name').value;
    resumeData.title = document.getElementById('input-title').value;
    resumeData.email = document.getElementById('input-email').value;
    resumeData.phone = document.getElementById('input-phone').value;
    resumeData.location = document.getElementById('input-location').value;
    resumeData.summary = document.getElementById('input-summary').value;
    resumeData.skills = document.getElementById('input-skills').value;

    const template = document.getElementById('template-select').value;
    const preview = document.getElementById('resume-preview');
    
    // Clear and set template class
    preview.className = `resume-paper template-${template}`;
    
    // Render based on template
    if (template === 'modern') {
        renderModern(preview);
    } else if (template === 'classic') {
        renderClassic(preview);
    } else if (template === 'creative') {
        renderCreative(preview);
    }
}

// --- TEMPLATE RENDERING FUNCTIONS ---

function renderModern(container) {
    container.innerHTML = `
        <header class="resume-header">
            <h1 contenteditable="true" onblur="syncFromPreview('name', this.innerText)">${resumeData.name || 'Your Name'}</h1>
            <div class="title" contenteditable="true" onblur="syncFromPreview('title', this.innerText)">${resumeData.title || 'Professional Title'}</div>
            <div class="contact-grid">
                <span contenteditable="true" onblur="syncFromPreview('email', this.innerText)">${resumeData.email || 'email@example.com'}</span>
                <span>•</span>
                <span contenteditable="true" onblur="syncFromPreview('phone', this.innerText)">${resumeData.phone || 'Phone'}</span>
                <span>•</span>
                <span contenteditable="true" onblur="syncFromPreview('location', this.innerText)">${resumeData.location || 'Location'}</span>
            </div>
        </header>

        <section class="resume-section">
            <h2 class="section-title">Summary</h2>
            <p contenteditable="true" onblur="syncFromPreview('summary', this.innerText)">${resumeData.summary || 'Summary text goes here...'}</p>
        </section>

        <section class="resume-section">
            <h2 class="section-title">Experience</h2>
            <div id="preview-experience">
                ${resumeData.experience.map((exp, i) => `
                    <div class="exp-item">
                        <div class="item-header">
                            <span class="item-role" contenteditable="true" onblur="syncListFromPreview('experience', ${i}, 'role', this.innerText)">${exp.role || 'Role'}</span>
                            <span class="item-date" contenteditable="true" onblur="syncListFromPreview('experience', ${i}, 'date', this.innerText)">${exp.date || 'Date'}</span>
                        </div>
                        <div class="item-company" contenteditable="true" onblur="syncListFromPreview('experience', ${i}, 'company', this.innerText)">${exp.company || 'Company'}</div>
                        <p class="item-desc" contenteditable="true" onblur="syncListFromPreview('experience', ${i}, 'description', this.innerText)">${exp.description || 'Job description...'}</p>
                    </div>
                `).join('')}
            </div>
        </section>

        <section class="resume-section">
            <h2 class="section-title">Education</h2>
            <div id="preview-education">
                ${resumeData.education.map((edu, i) => `
                    <div class="exp-item">
                        <div class="item-header">
                            <span class="item-role" contenteditable="true" onblur="syncListFromPreview('education', ${i}, 'degree', this.innerText)">${edu.degree || 'Degree'}</span>
                            <span class="item-date" contenteditable="true" onblur="syncListFromPreview('education', ${i}, 'date', this.innerText)">${edu.date || 'Date'}</span>
                        </div>
                        <div class="item-company" contenteditable="true" onblur="syncListFromPreview('education', ${i}, 'school', this.innerText)">${edu.school || 'School'}</div>
                        <p class="item-desc" contenteditable="true" onblur="syncListFromPreview('education', ${i}, 'description', this.innerText)">${edu.description || 'Description...'}</p>
                    </div>
                `).join('')}
            </div>
        </section>

        <section class="resume-section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-list">
                ${(resumeData.skills || '').split(',').map(s => s.trim() ? `<span class="skill-tag">${s.trim()}</span>` : '').join('')}
            </div>
        </section>
    `;
}

// Placeholder for other templates - keeping it simple for Modern first
function renderClassic(container) { renderModern(container); container.className += " template-classic"; }
function renderCreative(container) { renderModern(container); container.className += " template-creative"; }

// --- SIDEBAR MANAGEMENT ---

function renderSidebarItems() {
    const expList = document.getElementById('experience-list');
    const eduList = document.getElementById('education-list');
    
    // Preserve the "Add" buttons
    const addExpBtn = expList.querySelector('.add-btn');
    const addEduBtn = eduList.querySelector('.add-btn');
    
    // Clear dynamic items but keep the add button
    expList.querySelectorAll('.dynamic-item').forEach(el => el.remove());
    eduList.querySelectorAll('.dynamic-item').forEach(el => el.remove());

    resumeData.experience.forEach((exp, i) => {
        const div = document.createElement('div');
        div.className = 'dynamic-item';
        div.innerHTML = `
            <button class="remove-btn" onclick="removeItem('experience', ${i})">Delete</button>
            <div class="input-group">
                <label>Job Title</label>
                <input type="text" value="${exp.role}" oninput="updateListItem('experience', ${i}, 'role', this.value)">
            </div>
            <div class="input-group">
                <label>Company</label>
                <input type="text" value="${exp.company}" oninput="updateListItem('experience', ${i}, 'company', this.value)">
            </div>
            <div class="input-group">
                <label>Duration</label>
                <input type="text" value="${exp.date}" oninput="updateListItem('experience', ${i}, 'date', this.value)">
            </div>
            <div class="input-group">
                <label>Description</label>
                <textarea rows="3" oninput="updateListItem('experience', ${i}, 'description', this.value)">${exp.description}</textarea>
            </div>
        `;
        expList.insertBefore(div, addExpBtn);
    });

    resumeData.education.forEach((edu, i) => {
        const div = document.createElement('div');
        div.className = 'dynamic-item';
        div.innerHTML = `
            <button class="remove-btn" onclick="removeItem('education', ${i})">Delete</button>
            <div class="input-group">
                <label>Degree</label>
                <input type="text" value="${edu.degree}" oninput="updateListItem('education', ${i}, 'degree', this.value)">
            </div>
            <div class="input-group">
                <label>School</label>
                <input type="text" value="${edu.school}" oninput="updateListItem('education', ${i}, 'school', this.value)">
            </div>
            <div class="input-group">
                <label>Duration</label>
                <input type="text" value="${edu.date}" oninput="updateListItem('education', ${i}, 'date', this.value)">
            </div>
        `;
        eduList.insertBefore(div, addEduBtn);
    });
}

// --- SYNC FUNCTIONS ---

function syncFromPreview(field, value) {
    const input = document.getElementById(`input-${field}`);
    if (input) input.value = value;
    resumeData[field] = value;
}

function syncListFromPreview(list, index, field, value) {
    resumeData[list][index][field] = value;
    renderSidebarItems(); // Reflect change in sidebar
}

function updateListItem(list, index, field, value) {
    resumeData[list][index][field] = value;
    updatePreview();
}

function addExperience() {
    resumeData.experience.push({ role: '', company: '', date: '', description: '' });
    renderSidebarItems();
    updatePreview();
}

function addEducation() {
    resumeData.education.push({ degree: '', school: '', date: '', description: '' });
    renderSidebarItems();
    updatePreview();
}

function removeItem(list, index) {
    resumeData[list].splice(index, 1);
    renderSidebarItems();
    updatePreview();
}

function toggleAccordion(btn) {
    const item = btn.parentElement;
    const isActive = item.classList.contains('active');
    
    // Close others
    document.querySelectorAll('.accordion-item').forEach(el => el.classList.remove('active'));
    
    if (!isActive) {
        item.classList.add('active');
    }
}

function changeTemplate() {
    updatePreview();
}

// --- PDF EXPORT ---

function downloadPDF() {
    const element = document.getElementById('resume-preview');
    const options = {
        margin: 0,
        filename: `${resumeData.name || 'Resume'}_CV.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    // Temporarily hide edit markers if any
    html2pdf().from(element).set(options).save();
}
