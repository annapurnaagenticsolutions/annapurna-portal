
(function(){
  const DATA = window.MATH_DATA;
  const app = document.getElementById('app');
  const topNav = document.getElementById('topNav');
  const menuButton = document.getElementById('menuButton');
  const backToTop = document.getElementById('backToTop');
  const STORAGE_KEY = 'math-concepts-lab::progress';
  let activeStep = 0;
  const stepNames = ['See it','Number','Why','Solve','Try'];

  function esc(value){
    return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  }
  function progress(){
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
    catch { return {}; }
  }
  function saveProgress(state){ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  function markDone(id){ const p=progress(); p[id]=true; saveProgress(p); route(); }
  function isDone(id){ return !!progress()[id]; }
  function byGrade(grade){ return DATA.lessons.filter(l => l.grade === Number(grade)); }
  function findLesson(id){ return DATA.lessons.find(l => l.id === id); }
  function classInfo(grade){ return DATA.classes.find(c => c.grade === Number(grade)); }
  function pct(done,total){ return total ? Math.round(done/total*100) : 0; }
  function groupBy(items,key){ return items.reduce((acc,item)=>{ const k=item[key] || 'Lessons'; (acc[k] ||= []).push(item); return acc; },{}); }
  function gradeBand(grade){
    if(grade <= 2) return {title:'Class 1–2',label:'Playful Foundation',icon:'🍎 ⚽ 🔺',copy:'Objects, counting, shapes, simple words, and daily examples.'};
    if(grade <= 5) return {title:'Class 3–5',label:'Activity Math',icon:'🧱 🕒 ₹',copy:'Place value, operations, money, time, measurement, and grids.'};
    if(grade <= 8) return {title:'Class 6–8',label:'Bridge Math',icon:'📏 ∠ ▦',copy:'Number lines, fractions, algebra, geometry, and data handling.'};
    return {title:'Class 9–10',label:'Exam Readiness',icon:'📈 △ √',copy:'Formal concepts, graphs, formulas, trigonometry, and stepwise solving.'};
  }
  function classProgress(grade){ const lessons=byGrade(grade); const done=lessons.filter(l=>isDone(l.id)).length; return {done,total:lessons.length,percentage:pct(done,lessons.length)}; }
  function updateNav(){
    const current = location.hash || '#home';
    const links = [
      ['#home','Home'],['#classes','Classes'],['#activities','Activities'],['#bridge','Bridge'],['#exam','Exam'],['#tests','Tests'],['#map','Maps'],['#practice','Practice'],['#progress','Progress'],['#guide','Guide']
    ];
    topNav.innerHTML = links.map(([href,label]) => `<a href="${href}" class="${current.startsWith(href) ? 'active' : ''}">${label}</a>`).join('');
  }
  function route(){
    updateNav();
    const hash = (location.hash || '#home').slice(1);
    activeStep = 0;
    if(hash === 'home' || !hash) renderHome();
    else if(hash === 'classes') renderClasses();
    else if(hash.startsWith('class-')) renderClass(Number(hash.split('-')[1]));
    else if(hash.startsWith('lesson-')) renderLesson(hash.replace('lesson-',''));
    else if(hash === 'practice') renderPractice();
    else if(hash === 'activities') renderActivities();
    else if(hash === 'bridge') renderBridgeMode();
    else if(hash === 'exam') renderExamMode();
    else if(hash === 'tests') renderChapterTests();
    else if(hash === 'progress') renderProgress();
    else if(hash === 'map') renderMaps();
    else if(hash === 'guide') renderGuide();
    else renderHome();
    app.focus({preventScroll:true});
    scrollTo({top:0,behavior:'smooth'});
  }

  function renderHome(){
    const totalLessons = DATA.lessons.length;
    const totalDone = DATA.lessons.filter(l=>isDone(l.id)).length;
    const classCards = DATA.classes.map(c => renderClassCard(c)).join('');
    app.innerHTML = `
      <section class="hero">
        <div class="hero-main">
          <p class="eyebrow"> class 1–10 release</p>
          <h1>Learn Math one small step at a time.</h1>
          <p class="lead">Choose your class. Learn with accurate visuals, school number form, activities, bridge coaching, exam readiness, chapter mini tests, and progress tracking.</p>
          <div class="pill-row">
            <span class="pill">Visual + number side by side</span>
            <span class="pill">Class 1 to Class 10</span>
            <span class="pill">Activities, bridge coaching, exam mode, tests, progress</span>
          </div>
          <div class="hero-actions">
            <a class="btn primary" href="#classes">Pick your class</a>
            <a class="btn ghost" href="#lesson-c1-counting-1-to-10">Start Class 1 sample</a>
            <a class="btn ghost" href="#bridge">Class 6–8 bridge mode</a>
            <a class="btn ghost" href="#exam">Class 9–10 exam mode</a>
            <a class="btn ghost" href="#tests">Chapter mini tests</a>
          </div>
          <div class="stability-strip"><span>Free guided learning lab</span><span>No worksheet pack</span><span>GitHub Pages ready</span></div>
        </div>
        <aside class="side-card">
          <p class="eyebrow">Simple learning process</p>
          <h2>See → Number → Why → Solve → Try</h2>
          <ol class="use-steps">
            <li><strong>See it</strong><p>Start with objects, bars, grids, number lines, shapes, or graphs.</p></li>
            <li><strong>Number</strong><p>Convert the same idea into school/exam number form.</p></li>
            <li><strong>Why</strong><p>Understand the reason before memorising any rule.</p></li>
            <li><strong>Practice</strong><p>Answer, check, correct mistakes, and track progress.</p></li>
          </ol>
        </aside>
      </section>

      <section class="section" id="classes-list">
        <div class="section-head">
          <div><p class="eyebrow">Class-first navigation</p><h2>Pick your class</h2><p class="muted">The app is now arranged from Class 1 to Class 10 instead of mixing all topics together.</p></div>
          <a class="btn blue" href="#tests">Open chapter tests</a>
        </div>
        <div class="class-grid">${classCards}</div>
      </section>

      <section class="section">
        <div class="section-head"><div><p class="eyebrow">Grade-band design</p><h2>Different ages need different presentation</h2></div></div>
        <div class="grade-bands">
          ${[1,3,6,9].map(g=>{const b=gradeBand(g);return `<article class="band-card"><div class="band-visual">${b.icon}</div><strong>${b.title}</strong><span class="badge">${b.label}</span><p class="muted">${b.copy}</p></article>`}).join('')}
        </div>
      </section>

      <section class="section">
        <div class="stats-row">
          <div class="stat"><strong>${DATA.classes.length}</strong><span class="muted">classes</span></div>
          <div class="stat"><strong>${totalLessons}</strong><span class="muted">lessons</span></div>
          <div class="stat"><strong>${totalDone}</strong><span class="muted">completed</span></div>
          <div class="stat"><strong>${pct(totalDone,totalLessons)}%</strong><span class="muted">overall progress</span></div>
        </div>
      </section>`;
  }
  function renderClassCard(c){
    const pr = classProgress(c.grade);
    const band = gradeBand(c.grade);
    return `<a class="class-card" href="#class-${c.grade}" style="--classColor:${esc(c.color)}">
      <span class="class-number">${c.grade}</span>
      <h3>${esc(c.title)}</h3>
      <p>${esc(c.subtitle)}</p>
      <div class="pill-row"><span class="badge">${esc(band.label)}</span><span class="badge good">${pr.done}/${pr.total}</span></div>
      <div class="mini-progress" style="--value:${pr.percentage}%"><span></span></div>
    </a>`;
  }
  function renderClasses(){
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Class selector</p><h1>Choose your class</h1><p class="lead">Start with the right level. Each class has its own chapters, visuals, map, practice, and progress.</p></div><div class="hero-meter"><strong>${DATA.lessons.length} lessons</strong><div class="progress-bar" style="--value:${pct(DATA.lessons.filter(l=>isDone(l.id)).length,DATA.lessons.length)}%"><span></span></div><p class="muted">Overall progress</p></div></section><section class="section"><div class="class-grid">${DATA.classes.map(c=>renderClassCard(c)).join('')}</div></section>`;
  }
  function renderClass(grade){
    const c = classInfo(grade); if(!c){renderClasses(); return;}
    const lessons = byGrade(grade); const pr = classProgress(grade); const chapters = groupBy(lessons,'chapter'); const band = gradeBand(grade);
    app.innerHTML = `
      <section class="page-hero">
        <div><p class="eyebrow">${esc(band.label)}</p><h1>${esc(c.title)} Math</h1><p class="lead">${esc(c.goal)}</p><div class="pill-row"><span class="badge">${esc(c.subtitle)}</span><span class="badge good">${pr.done} of ${pr.total} completed</span></div></div>
        <div class="hero-meter"><strong>${pr.percentage}% complete</strong><div class="progress-bar" style="--value:${pr.percentage}%"><span></span></div><a class="btn small blue" href="#lesson-${lessons[0].id}">Start first lesson</a>${grade<=5?'<a class="btn small" href="#activities">Activity mode</a>':''}${grade>=6&&grade<=8?'<a class="btn small" href="#bridge">Bridge mode</a>':''}${grade>=9?'<a class="btn small" href="#exam">Exam mode</a>':''}</div>
      </section>
      <section class="section"><div class="class-map"><p class="eyebrow">Class learning map</p><div class="map-path">${Object.keys(chapters).map((ch,i)=>`${i?'<span class="map-arrow">→</span>':''}<span class="map-node">${esc(ch)}</span>`).join('')}</div></div></section>
      <section class="section"><div class="section-head"><div><p class="eyebrow">Chapters</p><h2>${esc(c.title)} lessons</h2></div><input class="search-box" id="lessonSearch" placeholder="Search lessons in this class" /></div><div id="lessonList">${renderChapterBlocks(chapters,c.color)}</div></section>`;
    const search = document.getElementById('lessonSearch');
    search?.addEventListener('input',()=>{
      const q=search.value.toLowerCase().trim();
      const filtered=lessons.filter(l=>`${l.title} ${l.summary} ${l.chapter}`.toLowerCase().includes(q));
      document.getElementById('lessonList').innerHTML = renderChapterBlocks(groupBy(filtered,'chapter'), c.color);
    });
  }
  function renderChapterBlocks(chapters,color){
    const names = Object.keys(chapters);
    if(!names.length) return `<div class="empty-state"><h3>No lesson found</h3><p class="muted">Try another search term.</p></div>`;
    return names.map(ch => `<div class="chapter-block"><h3 class="chapter-title">${esc(ch)}</h3><div class="lesson-grid">${chapters[ch].map(l=>renderLessonCard(l,color)).join('')}</div></div>`).join('');
  }
  function renderLessonCard(l,color){
    return `<a class="lesson-card" href="#lesson-${l.id}" style="--classColor:${color || classInfo(l.grade).color}">
      <div class="lesson-topline"><span class="lesson-icon">${esc(l.icon || l.visual?.icon || '∑')}</span><span class="badge ${isDone(l.id)?'good':''}">${isDone(l.id)?'Done':'Start'}</span></div>
      <h3>${esc(l.title)}</h3><p>${esc(l.summary)}</p>
    </a>`;
  }
  function renderLesson(id){
    const lesson = findLesson(id); if(!lesson){renderHome(); return;}
    const c=classInfo(lesson.grade); const lessons=byGrade(lesson.grade); const idx=lessons.findIndex(l=>l.id===lesson.id); const next=lessons[idx+1]; const prev=lessons[idx-1];
    app.innerHTML = `
      <article class="lesson-page" style="--classColor:${esc(c.color)}">
        <section class="lesson-hero">
          <div class="lesson-big-icon">${esc(lesson.icon || lesson.visual?.icon || '∑')}</div>
          <div><p class="eyebrow">${esc(c.title)} · ${esc(lesson.chapter)}</p><h1>${esc(lesson.title)}</h1><p class="lead">${esc(lesson.summary)}</p></div>
          <div class="lesson-toolbar"><a class="btn small" href="#class-${lesson.grade}">Back to class</a><button class="btn small blue" id="markDone">${isDone(lesson.id)?'Completed':'Mark complete'}</button></div>
        </section>
        <section class="learning-shell">
          <aside class="step-rail" id="stepRail">${stepNames.map((name,i)=>`<button class="step-tab ${i===activeStep?'active':''}" data-step="${i}"><span>${i+1}</span><b>${name}</b></button>`).join('')}</aside>
          <div><div id="lessonStage"></div></div>
        </section>
        <section class="info-grid">
          <div class="panel"><h3>Formula / number form</h3><div class="formula-box">${esc(lesson.formula || 'No formula needed')}</div>${renderFormulaParts(lesson)}</div>
          ${renderActivityPanel(lesson)}
          ${renderWordProblemPanel(lesson)}
          ${renderBridgeCoachPanel(lesson)}
          ${renderExamCoachPanel(lesson)}
          ${renderProofScaffoldPanel(lesson)}
          <div class="panel mistake"><h3>Mistake Coach</h3><p><strong>Wrong:</strong> ${esc(lesson.mistake?.wrong || 'Skipping steps.')}</p><p><strong>Correct:</strong> ${esc(lesson.mistake?.correct || 'Match visual, number, and answer.')}</p><p><strong>Why:</strong> ${esc(lesson.mistake?.why || 'Slow steps reduce errors.')}</p></div>
          <div class="panel teacher"><h3>Teacher / Parent Note</h3><p>${esc(lesson.teacherNote || 'Ask the learner to explain the visual before writing the number sentence.')}</p><div class="button-row">${prev?`<a class="btn small" href="#lesson-${prev.id}">← Previous</a>`:''}${next?`<a class="btn small blue" href="#lesson-${next.id}">Next →</a>`:''}</div></div>
        </section>
        <section class="section"><div class="panel"><h3>Worked example</h3>${renderWorkedExample(lesson)}<div class="habit-note"><strong>Good solving habit:</strong> write given values, show the operation, calculate slowly, then write the final answer.</div></div></section>
        <section class="section"><div class="panel"><h3>Try it now</h3>${renderPracticeBlock(lesson)}</div></section>${renderMicroPracticeSection(lesson)}${renderBridgeDrillSection(lesson)}${renderExamDrillSection(lesson)}
      </article>`;
    document.getElementById('markDone')?.addEventListener('click',()=>markDone(lesson.id));
    document.querySelectorAll('.step-tab').forEach(btn=>btn.addEventListener('click',()=>{activeStep=Number(btn.dataset.step); renderLessonStage(lesson); document.querySelectorAll('.step-tab').forEach(b=>b.classList.toggle('active', Number(b.dataset.step)===activeStep));}));
    renderLessonStage(lesson);
  }
  function renderLessonStage(lesson){
    const s = lesson.steps?.[activeStep] || lesson.steps?.[0] || {title:'See it',headline:lesson.title,body:lesson.summary,number:lesson.formula};
    const stage = document.getElementById('lessonStage'); if(!stage) return;
    stage.innerHTML = `<div class="learn-board"><div class="visual-board">${renderVisual(lesson.visual)}</div><div class="explain-board"><p class="eyebrow">Step ${activeStep+1} · ${esc(s.title)}</p><h2>${esc(s.headline)}</h2><p>${esc(s.body)}</p>${lesson.kidSentence && activeStep===0 ? `<div class="kid-sentence">${esc(lesson.kidSentence)}</div>` : ''}<div class="number-strip">${esc(s.number || lesson.formula || '')}</div><div class="quick-actions"><button class="btn ghost" id="prevStep">← Previous step</button><button class="btn primary" id="nextStep">Next step →</button></div></div></div>`;
    document.getElementById('prevStep')?.addEventListener('click',()=>{activeStep=Math.max(0,activeStep-1); renderLessonStage(lesson); updateStepRail();});
    document.getElementById('nextStep')?.addEventListener('click',()=>{activeStep=Math.min(stepNames.length-1,activeStep+1); renderLessonStage(lesson); updateStepRail();});
  }
  function updateStepRail(){ document.querySelectorAll('.step-tab').forEach(b=>b.classList.toggle('active', Number(b.dataset.step)===activeStep)); }
  function renderFormulaParts(l){
    if(!l.formulaParts?.length) return '';
    return `<ul>${l.formulaParts.map(p=>`<li><strong>${esc(p.symbol)}:</strong> ${esc(p.meaning)}</li>`).join('')}</ul>`;
  }

  function renderActivityPanel(l){
    if(!l.activity) return '';
    const a=l.activity;
    return `<div class="panel activity-panel"><h3>Activity Corner</h3><p class="muted">${esc(a.materials || 'Use simple objects or draw the idea.')}</p><div class="activity-steps"><p><strong>Do:</strong> ${esc(a.do)}</p><p><strong>Say:</strong> ${esc(a.say)}</p><p><strong>Write:</strong> ${esc(a.write)}</p><p><strong>Check:</strong> ${esc(a.check)}</p></div></div>`;
  }
  function renderWordProblemPanel(l){
    if(!l.wordProblem) return '';
    const w=l.wordProblem;
    return `<div class="panel word-panel"><h3>Word Problem Builder</h3><p><strong>Story:</strong> ${esc(w.story)}</p>${w.steps?.length?`<ol class="worked-list compact">${w.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol>`:''}<p><strong>Answer:</strong> ${esc(w.answer || '')}</p></div>`;
  }
  function renderMicroPracticeSection(l){
    if(!l.microPractice?.length) return '';
    return `<section class="section"><div class="panel"><div class="section-head tight"><div><p class="eyebrow">Foundation drill</p><h3>Two tiny checks</h3></div></div><div class="micro-grid">${l.microPractice.map((m,i)=>`<article class="micro-card"><span class="badge">Check ${i+1}</span><p><strong>${esc(m.prompt)}</strong></p><details><summary>Show hint and answer</summary><p><strong>Hint:</strong> ${esc(m.hint || 'Use the visual first.')}</p><p><strong>Answer:</strong> ${esc(m.answer || '')}</p></details></article>`).join('')}</div></div></section>`;
  }


  function renderBridgeCoachPanel(l){
    if(!l.bridgeCoach) return '';
    const b=l.bridgeCoach;
    return `<div class="panel bridge-panel"><h3>Bridge Coach</h3><div class="bridge-flow"><p><strong>Before this:</strong> ${esc(b.prerequisite)}</p><p><strong>Familiar idea:</strong> ${esc(b.concrete)}</p><p><strong>School form:</strong> ${esc(b.schoolForm)}</p><p><strong>Why it works:</strong> ${esc(b.whyItWorks)}</p><p><strong>Check:</strong> ${esc(b.check)}</p></div></div>`;
  }
  function renderBridgeDrillSection(l){
    if(!l.bridgeDrill?.length) return '';
    return `<section class="section"><div class="panel bridge-drill"><div class="section-head tight"><div><p class="eyebrow">Bridge drill</p><h3>From meaning to exam form</h3></div></div><div class="micro-grid">${l.bridgeDrill.map((m,i)=>`<article class="micro-card bridge-card"><span class="badge">Bridge ${i+1}</span><p><strong>${esc(m.prompt)}</strong></p><details><summary>Show hint and answer</summary><p><strong>Hint:</strong> ${esc(m.hint || 'Use the prerequisite and the visual first.')}</p><p><strong>Answer:</strong> ${esc(m.answer || '')}</p></details></article>`).join('')}</div></div></section>`;
  }


  function renderExamCoachPanel(l){
    if(!l.examCoach) return '';
    const e=l.examCoach;
    return `<div class="panel exam-panel"><h3>Exam Coach</h3><div class="exam-flow"><p><strong>Before this:</strong> ${esc(e.prerequisite)}</p><p><strong>Core idea:</strong> ${esc(e.coreIdea)}</p><p><strong>Exam form:</strong> ${esc(e.examForm)}</p><p><strong>Checkpoint:</strong> ${esc(e.checkpoint)}</p></div>${e.scoringSteps?.length?`<ol class="worked-list compact">${e.scoringSteps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol>`:''}<p class="exam-warning"><strong>Board mistake:</strong> ${esc(e.commonBoardMistake || '')}</p></div>`;
  }
  function renderProofScaffoldPanel(l){
    if(!l.proofScaffold) return '';
    const p=l.proofScaffold;
    return `<div class="panel proof-panel"><h3>${esc(p.title || 'Proof Scaffold')}</h3><ol class="worked-list compact">${(p.steps||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ol></div>`;
  }
  function renderExamDrillSection(l){
    if(!l.examDrill?.length) return '';
    return `<section class="section"><div class="panel exam-drill"><div class="section-head tight"><div><p class="eyebrow">Timed exam drill</p><h3>Short board-style checks</h3></div><span class="badge warn">2–4 minutes</span></div><div class="micro-grid">${l.examDrill.map((m,i)=>`<article class="micro-card exam-card"><span class="badge">Exam ${i+1}</span><p><strong>${esc(m.prompt)}</strong></p><details><summary>Show hint and answer</summary><p><strong>Hint:</strong> ${esc(m.hint || 'Write formula first, then substitute.')}</p><p><strong>Answer:</strong> ${esc(m.answer || '')}</p></details></article>`).join('')}</div></div></section>`;
  }

  function renderWorkedExample(l){
    const w=l.workedExample || {};
    return `<p><strong>Question:</strong> ${esc(w.question || l.practice?.question || '')}</p>${w.given?.length?`<p><strong>Given:</strong></p><ul>${w.given.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}${w.steps?.length?`<ol class="worked-list">${w.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol>`:''}<p><strong>Answer:</strong> ${esc(w.answer || l.practice?.answer || '')}</p>`;
  }
  function renderPracticeBlock(l){
    const p=l.practice || {}; const opts=p.options || [];
    return `<p><strong>${esc(p.question || 'Practice question')}</strong></p><div class="practice-options">${opts.map(o=>`<button class="practice-choice" data-answer="${esc(o)}">${esc(o)}</button>`).join('')}</div>${p.hint?`<details class="hint-box"><summary>Need a hint?</summary><p>${esc(p.hint)}</p></details>`:''}<div class="feedback" role="status" aria-live="polite" hidden></div>`;
  }
  app.addEventListener('click', event => {
    const choice = event.target.closest('.practice-choice,.exam-choice'); if(!choice) return;
    const card = choice.closest('.panel,.practice-card');
    const lessonId = card?.dataset.lessonId;
    let correct = '';
    let explanation = '';
    if(lessonId){ const l=findLesson(lessonId); correct=l?.practice?.answer || ''; explanation=l?.practice?.explanation || ''; }
    else { const title = document.querySelector('.lesson-hero h1')?.textContent; const l=DATA.lessons.find(x=>x.title===title); correct=l?.practice?.answer || ''; explanation=l?.practice?.explanation || ''; }
    const selected = choice.dataset.answer;
    const ok = String(selected).trim() === String(correct).trim();
    choice.classList.add(ok?'correct':'wrong');
    const feedback = card?.querySelector('.feedback') || document.getElementById('practiceFeedback');
    if(feedback){ feedback.hidden=false; feedback.textContent = ok ? `Correct. ${explanation || 'Good. The visual and number form match.'}` : `Not yet. Correct answer: ${correct}. ${explanation || 'Go back to See it and Number steps.'}`; }
  });
  function renderPractice(){
    const sample = DATA.lessons.filter((_,i)=>i%3===0 || i<10).slice(0,42);
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Practice mode</p><h1>Practice by class</h1><p class="lead">Short questions with instant feedback. This is not a full exam; it is quick revision.</p></div><div class="hero-meter"><strong>${sample.length} quick questions</strong><p class="muted">Selected across Class 1–10</p></div></section><section class="section"><div class="practice-grid">${sample.map(l=>`<article class="practice-card" data-lesson-id="${l.id}"><span class="badge">Class ${l.grade}</span><h3>${esc(l.title)}</h3>${renderPracticeBlock(l)}</article>`).join('')}</div></section>`;
  }

  function renderActivities(){
    const foundation = DATA.lessons.filter(l => l.grade <= 5 && l.activity);
    const byG = foundation.reduce((acc,l)=>{ (acc[l.grade] ||= []).push(l); return acc; },{});
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Class 1–5 activity mode</p><h1>Learn by doing, saying, writing, and checking.</h1><p class="lead">This page collects the hands-on parts from foundational lessons. It is useful for parents, teachers, and young learners before solving formal questions.</p></div><div class="hero-meter"><strong>${foundation.length} activities</strong><p class="muted">Objects, clocks, money, bars, grids, and word problems.</p></div></section><section class="section"><div class="activity-class-list">${Object.keys(byG).map(g=>`<article class="activity-class"><div class="section-head tight"><div><p class="eyebrow">Class ${g}</p><h2>${esc(classInfo(g).subtitle)}</h2></div><a class="btn small blue" href="#class-${g}">Open class</a></div><div class="activity-card-grid">${byG[g].map(l=>`<a class="activity-card" href="#lesson-${l.id}"><span class="badge">${esc(l.chapter)}</span><h3>${esc(l.title)}</h3><p><strong>Do:</strong> ${esc(l.activity.do)}</p><p><strong>Write:</strong> ${esc(l.activity.write)}</p></a>`).join('')}</div></article>`).join('')}</div></section>`;
  }


  function renderBridgeMode(){
    const bridge = DATA.lessons.filter(l => l.grade >= 6 && l.grade <= 8 && l.bridgeCoach);
    const byG = bridge.reduce((acc,l)=>{ (acc[l.grade] ||= []).push(l); return acc; },{});
    const persona = DATA.personaReview || {};
    app.innerHTML = `<section class="page-hero bridge-hero"><div><p class="eyebrow">Class 6–8 bridge mode</p><h1>Move from arithmetic to abstract math without fear.</h1><p class="lead">This page collects bridge lessons for integers, rational numbers, algebra, geometry, graphs, mensuration, and data. Each lesson starts with what the learner already knows, then moves to school form.</p><div class="pill-row"><span class="pill">Prerequisite reminder</span><span class="pill">Why the rule works</span><span class="pill">Misconception check</span></div></div><div class="hero-meter"><strong>${bridge.length} bridge lessons</strong><p class="muted">Classes 6, 7, and 8.</p></div></section><section class="section"><div class="persona-card"><p class="eyebrow">Persona alignment review</p><h2>${esc(persona.persona || 'Bridge Math Teacher')}</h2><p>${esc(persona.alignment || '')}</p><div class="persona-checks">${(persona.reviewQuestions||[]).map(q=>`<span>${esc(q)}</span>`).join('')}</div></div></section><section class="section"><div class="activity-class-list">${Object.keys(byG).map(g=>`<article class="activity-class bridge-class"><div class="section-head tight"><div><p class="eyebrow">Class ${g}</p><h2>${esc(classInfo(g).subtitle)}</h2></div><a class="btn small blue" href="#class-${g}">Open class</a></div><div class="activity-card-grid">${byG[g].map(l=>`<a class="activity-card bridge-link" href="#lesson-${l.id}"><span class="badge">${esc(l.chapter)}</span><h3>${esc(l.title)}</h3><p><strong>Before:</strong> ${esc(l.bridgeCoach.prerequisite)}</p><p><strong>School:</strong> ${esc(l.bridgeCoach.schoolForm)}</p><p><strong>Misconception:</strong> ${esc(l.mistake?.wrong || '')}</p></a>`).join('')}</div></article>`).join('')}</div></section>`;
  }


  function renderExamMode(){
    const exam = DATA.lessons.filter(l => l.grade >= 9 && l.examCoach);
    const byG = exam.reduce((acc,l)=>{ (acc[l.grade] ||= []).push(l); return acc; },{});
    const persona = DATA.personaReviewV19 || DATA.examReadiness || {};
    app.innerHTML = `<section class="page-hero exam-hero"><div><p class="eyebrow">Class 9–10 exam mode</p><h1>Turn understanding into board-style answers.</h1><p class="lead">This page collects high-school lessons with formula maps, proof scaffolds, scoring steps, and timed drills. It is designed for revision after the learner understands the idea.</p><div class="pill-row"><span class="pill">Formula maps</span><span class="pill">Proof scaffolds</span><span class="pill">Timed drills</span><span class="pill">Mistake coach</span></div></div><div class="hero-meter"><strong>${exam.length} exam-ready lessons</strong><p class="muted">Classes 9 and 10.</p></div></section><section class="section"><div class="persona-card exam-persona"><p class="eyebrow">Persona alignment review</p><h2>${esc(persona.persona || 'Exam Math Mentor')}</h2><p>${esc(persona.alignment || persona.focus || '')}</p><div class="persona-checks">${(persona.reviewQuestions||persona.principles||[]).map(q=>`<span>${esc(q)}</span>`).join('')}</div></div></section><section class="section"><div class="exam-checklist"><h2>Exam answer habit</h2><div class="check-grid"><span>1. Read what is asked</span><span>2. Write given values</span><span>3. State formula/theorem</span><span>4. Substitute carefully</span><span>5. Simplify line by line</span><span>6. Write final answer/unit/reason</span></div></div></section><section class="section"><div class="activity-class-list">${Object.keys(byG).map(g=>`<article class="activity-class exam-class"><div class="section-head tight"><div><p class="eyebrow">Class ${g}</p><h2>${esc(classInfo(g).subtitle)}</h2></div><a class="btn small blue" href="#class-${g}">Open class</a></div><div class="activity-card-grid">${byG[g].map(l=>`<a class="activity-card exam-link" href="#lesson-${l.id}"><span class="badge">${esc(l.chapter)}</span><h3>${esc(l.title)}</h3><p><strong>Formula:</strong> ${esc(l.examCoach.examForm)}</p><p><strong>Board mistake:</strong> ${esc(l.examCoach.commonBoardMistake || '')}</p></a>`).join('')}</div></article>`).join('')}</div></section>`;
  }


  function renderChapterTests(){
    const byGradeChapter = {};
    DATA.lessons.forEach(l => {
      byGradeChapter[l.grade] ||= {};
      byGradeChapter[l.grade][l.chapter] ||= [];
      byGradeChapter[l.grade][l.chapter].push(l);
    });
    const totalChapters = Object.values(byGradeChapter).reduce((sum, chapters) => sum + Object.keys(chapters).length, 0);
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Chapter mini tests</p><h1>Check one chapter at a time.</h1><p class="lead">These are lightweight in-page tests built from existing lesson practice questions. They keep the product focused on learning inside the lab, not worksheet downloads.</p><div class="pill-row"><span class="badge">Class-wise</span><span class="badge">Chapter-wise</span><span class="badge">Instant feedback</span></div></div><div class="hero-meter"><strong>${totalChapters} chapter checks</strong><p class="muted">No printable worksheet pack in .</p></div></section><section class="section"><div class="qa-grid"><article class="qa-card"><strong>${DATA.classes.length}</strong><span class="muted">classes</span></article><article class="qa-card"><strong>${DATA.lessons.length}</strong><span class="muted">lessons</span></article><article class="qa-card"><strong>${totalChapters}</strong><span class="muted">chapter checks</span></article><article class="qa-card"><strong>0</strong><span class="muted">download packs</span></article></div></section><section class="section"><div class="activity-class-list">${Object.keys(byGradeChapter).map(g=>{ const c=classInfo(g); const chapters=byGradeChapter[g]; return `<article class="test-class"><div class="section-head tight"><div><p class="eyebrow">Class ${g}</p><h2>${esc(c.subtitle)}</h2></div><a class="btn small blue" href="#class-${g}">Open class</a></div><div class="test-grid">${Object.keys(chapters).map(ch=>{ const lessons=chapters[ch]; const qs=lessons.slice(0,3); return `<article class="test-card"><span class="badge">${qs.length} questions</span><h3>${esc(ch)}</h3><p class="muted">Quick check using lessons from this chapter.</p><details><summary>Start mini test</summary>${qs.map((l,i)=>`<div class="chapter-question" data-lesson-id="${l.id}"><h4>Q${i+1}. ${esc(l.title)}</h4>${renderPracticeBlock(l)}</div>`).join('')}</details></article>` }).join('')}</div></article>` }).join('')}</div></section>`;
  }

  function renderProgress(){
    const total=DATA.lessons.length, done=DATA.lessons.filter(l=>isDone(l.id)).length;
    const achievements = [
      ['🌱','Starter','Complete any 5 lessons',done>=5],['🍎','Foundation Builder','Complete Class 1 or 2',classProgress(1).percentage===100 || classProgress(2).percentage===100],['▰','Fraction Builder',DATA.lessons.some(l=>isDone(l.id)&&l.title.toLowerCase().includes('fraction'))],['📈','Graph Explorer',DATA.lessons.some(l=>isDone(l.id)&&/graph|coordinate/i.test(l.title))],['△','Geometry Learner',DATA.lessons.some(l=>isDone(l.id)&&/triangle|circle|angle/i.test(l.title))],['√','Exam Ready Path','Complete 20+ lessons',done>=20]
    ];
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Progress</p><h1>Your learning dashboard</h1><p class="lead">Track class-wise progress and badges. Progress is stored locally in this browser.</p></div><div class="hero-meter"><strong>${done}/${total} completed</strong><div class="progress-bar" style="--value:${pct(done,total)}%"><span></span></div><p class="muted">Overall progress</p></div></section><section class="section"><div class="progress-grid">${DATA.classes.map(c=>{const pr=classProgress(c.grade);return `<article class="progress-card"><h3>${esc(c.title)}</h3><div class="progress-bar" style="--value:${pr.percentage}%"><span></span></div><p class="muted">${pr.done} of ${pr.total} lessons · ${pr.percentage}%</p><a class="btn small" href="#class-${c.grade}">Open class</a></article>`}).join('')}</div></section><section class="section"><div class="section-head"><div><p class="eyebrow">Motivation</p><h2>Badges</h2></div></div><div class="achievement-grid">${achievements.map(([icon,title,copy,unlocked])=>`<article class="achievement"><div class="medal">${icon}</div><h3>${title}</h3><p class="muted">${copy}</p><span class="badge ${unlocked?'good':'warn'}">${unlocked?'Unlocked':'Locked'}</span></article>`).join('')}</div></section>`;
  }
  function renderMaps(){
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Learning maps</p><h1>See how topics connect</h1><p class="lead">Each class map shows the chapter flow. This helps learners know what comes first and what comes next.</p></div><a class="btn blue" href="#classes">Pick a class</a></section><section class="section"><div class="map-grid">${DATA.classes.map(c=>{const chapters=Object.keys(groupBy(byGrade(c.grade),'chapter'));return `<article class="map-card"><h3>${esc(c.title)}</h3><p class="muted">${esc(c.subtitle)}</p><div class="map-path">${chapters.map((ch,i)=>`${i?'<span class="map-arrow">→</span>':''}<a class="map-node" href="#class-${c.grade}">${esc(ch)}</a>`).join('')}</div></article>`}).join('')}</div></section>`;
  }
  function renderGuide(){
    app.innerHTML = `<section class="page-hero"><div><p class="eyebrow">Guide</p><h1>How to use this lab</h1><p class="lead"> is the stable Class 1–10 release. Use class-wise learning, activities, bridge coaching, exam readiness, chapter mini tests, and progress tracking. Printable worksheets are intentionally excluded in this version.</p></div></section><section class="section"><div class="info-grid"><div class="panel"><h3>For Class 1–2</h3><p>Ask the learner to count objects aloud. Do not rush to symbols.</p></div><div class="panel"><h3>For Class 3–5</h3><p>Use grids, bars, money, clocks, and step-by-step word problems.</p></div><div class="panel bridge-panel"><h3>For Class 6–8</h3><p>Use the Bridge Coach: prerequisite → familiar idea → school form → why → slow solve → misconception check.</p></div><div class="panel"><h3>For Class 9–10</h3><p>Use graphs, formulas, and structured exam-style solutions.</p></div><div class="panel mistake"><h3>Rule for visuals</h3><p>Visual, number sentence, explanation, and answer must match exactly.</p></div><div class="panel teacher"><h3>Teacher mode</h3><p>First ask: “What do you see?” Then ask: “How will you write it as numbers?”</p></div></div></section>`;
  }

  function renderVisual(v){
    if(!v) return '';
    switch(v.type){
      case 'objects': return objects(v);
      case 'arithmetic': return arithmetic(v);
      case 'compare': return compareVisual(v);
      case 'length': return lengthVisual(v);
      case 'pattern': return patternVisual(v);
      case 'moneyAdd': return moneyAdd(v);
      case 'fractionAdd': return fractionAdd(v);
      case 'decimalAdd': return decimalAdd(v);
      case 'equationBalance': return equationBalance(v);
      case 'placeValueTable': return placeValueTable(v);
      case 'symmetry': return symmetry(v);
      case 'placeValue': return placeValue(v);
      case 'numberLine': return numberLine(v);
      case 'fraction': return fraction(v);
      case 'grid': return grid(v);
      case 'array': return arrayVisual(v);
      case 'division': return division(v);
      case 'shape': return shape(v);
      case 'clock': return clock(v);
      case 'money': return money(v);
      case 'barChart': return barChart(v);
      case 'coordinate': return coordinate(v);
      case 'triangle': return triangle(v);
      case 'angle': return angle(v);
      case 'conceptMap': return conceptMap(v);
      default: return conceptMap({nodes:['See','Number','Solve']});
    }
  }
  function objects(v){ return `<div><div class="object-row">${Array.from({length:v.count||0},()=>`<span class="object">${esc(v.emoji||v.icon||'●')}</span>`).join('')}</div><p class="visual-caption">${esc(v.count)} ${esc(v.label||'objects')}</p></div>`; }
  function arithmetic(v){ const max=14; const left=Array.from({length:Math.min(v.left||0,max)},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join(''); const right=Array.from({length:Math.min(v.right||0,max)},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join(''); const result=Array.from({length:Math.min(v.result||0,max)},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join(''); return `<div><div class="arith-line"><span>${left}</span><span class="arith-symbol">${esc(v.op)}</span><span>${right}</span><span class="arith-symbol">=</span><span>${result}</span></div><p class="visual-caption">${esc(v.left)} ${esc(v.op)} ${esc(v.right)} = ${esc(v.result)}</p></div>`; }

  function compareVisual(v){
    const left=Array.from({length:v.left||0},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join('');
    const right=Array.from({length:v.right||0},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join('');
    return `<div class="compare-demo"><div class="compare-box"><b>${esc(v.leftLabel||v.left)}</b><div>${left}</div></div><div class="compare-symbol">&gt;</div><div class="compare-box"><b>${esc(v.rightLabel||v.right)}</b><div>${right}</div></div><p class="visual-caption">${esc(v.left)} is greater than ${esc(v.right)}</p></div>`;
  }
  function lengthVisual(v){
    const bars=v.bars||[50,100]; const labels=v.labels||bars.map((_,i)=>`bar ${i+1}`);
    return `<div class="length-demo">${bars.map((w,i)=>`<div class="length-row"><span>${esc(labels[i])}</span><b style="width:${Math.max(24,w)}%"></b></div>`).join('')}<p class="visual-caption">Compare from the same starting line.</p></div>`;
  }
  function patternVisual(v){
    return `<div class="pattern-demo">${(v.items||[]).map(x=>`<span>${esc(x)}</span>`).join('')}</div><p class="visual-caption">Find the repeat rule.</p>`;
  }
  function moneyAdd(v){
    return `<div class="money-add"><span class="money-note">₹${esc(v.left)}</span><span class="arith-symbol">+</span><span class="money-note">₹${esc(v.right)}</span><span class="arith-symbol">=</span><span class="money-note result">₹${esc(v.result)}</span></div>`;
  }
  function fractionAdd(v){
    const bar=(filled)=>`<div class="fbar" style="--parts:${v.parts||5}">${Array.from({length:v.parts||5},(_,i)=>`<span class="fseg ${i<filled?'fill':''}"></span>`).join('')}</div>`;
    return `<div class="fraction-add"><div>${bar(v.leftFilled||0)}<small>first fraction</small></div><span class="arith-symbol">+</span><div>${bar(v.rightFilled||0)}<small>second fraction</small></div><span class="arith-symbol">=</span><div>${bar(v.resultFilled||0)}<small>result</small></div><p class="visual-caption">${esc(v.expression||'fraction addition')}</p></div>`;
  }
  function decimalAdd(v){
    return `<div class="decimal-add"><table><tr><th>ones</th><th>.</th><th>tenths</th></tr><tr><td>${esc(String(v.left).split('.')[0])}</td><td>.</td><td>${esc(String(v.left).split('.')[1]||'0')}</td></tr><tr><td>${esc(String(v.right).split('.')[0])}</td><td>.</td><td>${esc(String(v.right).split('.')[1]||'0')}</td></tr><tr class="result"><td>${esc(String(v.result).split('.')[0])}</td><td>.</td><td>${esc(String(v.result).split('.')[1]||'0')}</td></tr></table><p class="visual-caption">Line up decimal points.</p></div>`;
  }
  function equationBalance(v){
    return `<div class="balance-demo"><div class="pan"><strong>${esc(v.left)}</strong></div><div class="fulcrum">⚖</div><div class="pan"><strong>${esc(v.right)}</strong></div><p class="visual-caption">Balanced when ${esc(v.answer||'both sides match')}</p></div>`;
  }
  function placeValueTable(v){
    return `<div class="place-table"><table><tr>${(v.places||[]).map(p=>`<th>${esc(p)}</th>`).join('')}</tr><tr>${(v.digits||[]).map(d=>`<td>${esc(d)}</td>`).join('')}</tr></table><p class="visual-caption">Read each digit by its place.</p></div>`;
  }
  function symmetry(v){
    return `<div class="symmetry-demo"><svg viewBox="0 0 640 420"><rect x="160" y="80" width="320" height="260" rx="24" fill="#dbeafe" stroke="#172554" stroke-width="6"/><line x1="320" y1="70" x2="320" y2="350" stroke="#ef4444" stroke-width="6" stroke-dasharray="12 12"/><text x="320" y="390" text-anchor="middle" font-size="26" font-weight="950">left half = right half</text></svg></div>`;
  }

  function placeValue(v){ function rep(n,cls){return Array.from({length:Math.max(0,n||0)},()=>`<span class="${cls}"></span>`).join('')} return `<div class="pv-wrap"><div class="pv-col"><div class="pv-items">${rep(v.hundreds,'hundred')}</div><b>${v.hundreds||0} hundreds</b></div><div class="pv-col"><div class="pv-items">${rep(v.tens,'ten')}</div><b>${v.tens||0} tens</b></div><div class="pv-col"><div class="pv-items">${rep(v.ones,'one')}</div><b>${v.ones||0} ones</b></div></div>`; }
  function numberLine(v){ const W=820,H=190,start=Number(v.start??0),end=Number(v.end??10),range=end-start || 1; const step=Math.max(1,Math.ceil(Math.abs(range)/10)); let ticks=''; for(let n=start;n<=end;n+=step){ const x=50+(n-start)/range*(W-100); ticks += `<line x1="${x}" y1="92" x2="${x}" y2="110" stroke="#172554" stroke-width="3"/><text x="${x}" y="140" text-anchor="middle" font-size="19" font-weight="900">${n}</text>`;} const pts=(v.points||[]).map(p=>{const x=50+(p-start)/range*(W-100); return `<circle cx="${x}" cy="92" r="13" fill="#2563eb"/><text x="${x}" y="58" text-anchor="middle" font-size="22" font-weight="950" fill="#172554">${esc(p)}</text>`}).join(''); return `<div class="numberline"><svg viewBox="0 0 ${W} ${H}"><line x1="50" y1="92" x2="770" y2="92" stroke="#172554" stroke-width="6" stroke-linecap="round"/>${ticks}${pts}</svg></div>`; }
  function fraction(v){ const parts=Math.max(1,v.parts||2), filled=Math.max(0,Math.min(parts,v.filled||0)); return `<div class="fraction-demo"><div class="fraction-bars"><div class="fbar" style="--parts:${parts}">${Array.from({length:parts},(_,i)=>`<span class="fseg ${i<filled?'fill':''}"></span>`).join('')}</div></div><p class="visual-caption">${esc(v.expression||`${filled}/${parts}`)}</p><p class="muted" style="text-align:center">${esc(v.label || 'Exact fraction bar')}</p></div>`; }
  function grid(v){ const rows=v.rows||10, cols=v.cols||10, total=rows*cols; return `<div><div class="grid-demo" style="grid-template-columns:repeat(${cols},24px)">${Array.from({length:total},(_,i)=>`<span class="grid-cell ${i<(v.filled||0)?'fill':''}"></span>`).join('')}</div><p class="visual-caption">${esc(v.expression||'grid')}</p></div>`; }
  function arrayVisual(v){ const rows=v.rows||1, cols=v.cols||1; return `<div><div class="array-demo" style="grid-template-columns:repeat(${cols},44px)">${Array.from({length:rows*cols},()=>`<span class="array-dot">${esc(v.emoji||'●')}</span>`).join('')}</div><p class="visual-caption">${rows} × ${cols} = ${rows*cols}</p></div>`; }
  function division(v){ const total=v.total||0, groups=Math.max(1,v.groups||1), per=Math.floor(total/groups), rem=total%groups; return `<div><div class="division-demo">${Array.from({length:groups},(_,g)=>`<div class="basket">${Array.from({length:per+(g<rem?1:0)},()=>`<span class="object">${esc(v.emoji||'●')}</span>`).join('')}<p><b>Group ${g+1}</b></p></div>`).join('')}</div><p class="visual-caption">${total} ÷ ${groups} = ${total/groups}</p></div>`; }
  function money(v){ return `<div class="concept-map"><span class="concept-node">₹${esc(v.amount||0)}</span><span class="arrow">=</span><span class="concept-node">Money value</span></div>`; }
  function conceptMap(v){ const nodes=v.nodes||['See','Number','Solve']; return `<div class="concept-map">${nodes.map((n,i)=>`${i?'<span class="arrow">→</span>':''}<span class="concept-node">${esc(n)}</span>`).join('')}</div>`; }
  function barChart(v){ const vals=v.values||[1,2,3], labels=v.labels||vals.map((_,i)=>String(i+1)), max=Math.max(...vals,1); return `<svg viewBox="0 0 760 440" width="100%" role="img" aria-label="bar chart"><rect x="40" y="30" width="680" height="360" rx="28" fill="#fff" stroke="#dbeafe"/><line x1="100" y1="350" x2="680" y2="350" stroke="#172554" stroke-width="4"/><line x1="100" y1="70" x2="100" y2="350" stroke="#172554" stroke-width="4"/>${vals.map((val,i)=>{const h=val/max*240,x=140+i*(500/Math.max(1,vals.length-1)),y=350-h;return `<rect x="${x}" y="${y}" width="72" height="${h}" rx="14" fill="#2563eb"/><text x="${x+36}" y="${y-12}" text-anchor="middle" font-weight="950">${val}</text><text x="${x+36}" y="382" text-anchor="middle" font-weight="900">${esc(labels[i])}</text>`}).join('')}</svg>`; }
  function coordinate(v){ const pts=v.points||[], W=720,H=460; const X=x=>90+(Number(x)+5)/10*(W-160), Y=y=>370-(Number(y)+5)/10*300; let path=''; if(v.line && pts.length>1) path += `<polyline points="${pts.map(p=>`${X(p[0])},${Y(p[1])}`).join(' ')}" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>`; if(v.parabola){ const curve=[]; for(let x=-4.5;x<=4.5;x+=.2) curve.push(`${X(x)},${Y((x*x)/3-2)}`); path += `<polyline points="${curve.join(' ')}" fill="none" stroke="#7c3aed" stroke-width="5"/>`; } return `<div class="coord"><svg viewBox="0 0 ${W} ${H}"><rect x="50" y="35" width="620" height="370" rx="26" fill="#fff" stroke="#dbeafe"/>${Array.from({length:11},(_,i)=>`<line x1="${90+i*52}" y1="65" x2="${90+i*52}" y2="370" stroke="#e2e8f0"/><line x1="90" y1="${70+i*30}" x2="610" y2="${70+i*30}" stroke="#e2e8f0"/>`).join('')}<line x1="90" y1="220" x2="610" y2="220" stroke="#172554" stroke-width="3"/><line x1="350" y1="65" x2="350" y2="370" stroke="#172554" stroke-width="3"/>${path}${pts.map(p=>`<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="10" fill="#ef4444"/><text x="${X(p[0])+14}" y="${Y(p[1])-12}" font-weight="950">(${esc(p[0])},${esc(p[1])})</text>`).join('')}</svg></div>`; }
  function shape(v){ const k=v.kind||'shape'; let body=''; if(k.includes('circle')) body=`<circle cx="310" cy="210" r="125" fill="#dbeafe" stroke="#172554" stroke-width="6"/>${k==='circle-tangent'?'<line x1="435" y1="80" x2="435" y2="340" stroke="#ef4444" stroke-width="6"/><line x1="310" y1="210" x2="435" y2="210" stroke="#172554" stroke-width="4"/>':''}`; else if(k==='triangle') body='<polygon points="310,65 115,340 535,340" fill="#dbeafe" stroke="#172554" stroke-width="6"/>'; else if(k==='rectangle') body='<rect x="125" y="120" width="390" height="210" rx="18" fill="#dbeafe" stroke="#172554" stroke-width="6"/>'; else if(k==='square') body='<rect x="190" y="80" width="280" height="280" rx="18" fill="#dbeafe" stroke="#172554" stroke-width="6"/>'; else if(k==='cuboid'||k==='cube') body='<polygon points="170,150 390,150 505,245 285,245" fill="#bfdbfe" stroke="#172554" stroke-width="4"/><polygon points="285,245 505,245 505,355 285,355" fill="#93c5fd" stroke="#172554" stroke-width="4"/><polygon points="170,150 285,245 285,355 170,260" fill="#dbeafe" stroke="#172554" stroke-width="4"/>'; else body='<polygon points="160,120 450,100 525,285 250,350" fill="#dbeafe" stroke="#172554" stroke-width="6"/>'; return `<div class="shape"><svg viewBox="0 0 640 440">${body}<text x="320" y="410" text-anchor="middle" font-weight="950" font-size="28">${esc(k)}</text></svg></div>`; }
  function clock(v){ const hour=Number(v.hour||0), minute=Number(v.minute||0); const ha=(hour%12)*30+minute*.5-90, ma=minute*6-90; const endpoint=(a,len)=>{const r=a*Math.PI/180; return [320+Math.cos(r)*len,220+Math.sin(r)*len];}; const hp=endpoint(ha,86), mp=endpoint(ma,125); return `<div class="clock"><svg viewBox="0 0 640 440"><circle cx="320" cy="220" r="155" fill="#fff" stroke="#172554" stroke-width="6"/>${Array.from({length:12},(_,i)=>{const p=endpoint((i+1)*30-90,128);return `<text x="${p[0]}" y="${p[1]+8}" text-anchor="middle" font-weight="950" font-size="22">${i+1}</text>`}).join('')}<line x1="320" y1="220" x2="${hp[0]}" y2="${hp[1]}" stroke="#172554" stroke-width="8" stroke-linecap="round"/><line x1="320" y1="220" x2="${mp[0]}" y2="${mp[1]}" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/><circle cx="320" cy="220" r="10" fill="#ef4444"/></svg></div>`; }
  function angle(v){ const deg=Number(v.degrees||60), rad=-deg*Math.PI/180, x=320+Math.cos(rad)*190, y=315+Math.sin(rad)*190; return `<div class="angle"><svg viewBox="0 0 640 440"><line x1="320" y1="315" x2="520" y2="315" stroke="#172554" stroke-width="8" stroke-linecap="round"/><line x1="320" y1="315" x2="${x}" y2="${y}" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/><path d="M385 315 A65 65 0 0 0 ${320+Math.cos(rad)*65} ${315+Math.sin(rad)*65}" fill="none" stroke="#ef4444" stroke-width="5"/><text x="372" y="272" font-size="34" font-weight="950">${deg}°</text></svg></div>`; }
  function triangle(v){ return `<div class="shape"><svg viewBox="0 0 640 440"><polygon points="160,350 520,350 520,95" fill="#dbeafe" stroke="#172554" stroke-width="6"/><text x="340" y="388" text-anchor="middle" font-weight="950">adjacent</text><text x="540" y="230" font-weight="950">opposite</text><text x="320" y="195" font-weight="950">hypotenuse</text><path d="M488 350 L488 318 L520 318" fill="none" stroke="#ef4444" stroke-width="4"/><text x="195" y="330" font-size="32" font-weight="950">θ</text></svg></div>`; }

  window.addEventListener('hashchange', route);
  menuButton?.addEventListener('click',()=>topNav.classList.toggle('open'));
  backToTop?.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
  route();
})();

