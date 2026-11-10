import { useState } from 'react'
import { ArrowDownRight, ArrowRight, ArrowUpRight, BarChart3, Check, ChevronRight, Database, Download, FileSpreadsheet, Github, Menu, ShieldCheck, Sparkles, X, Zap } from 'lucide-react'

const cases = [
  { id:'01', tag:'PROJECT FINANCE', title:'Ubon Chili Cold Storage Project', desc:'Evaluate a regional cold-storage facility built around agricultural supply chains in Ubon Ratchathani. Turn operational assumptions into an investment decision.', level:'Advanced', color:'mint', skills:['CAPEX & OPEX','WACC','Project NPV / IRR','Scenario analysis'], metric:'฿48.0M', metricLabel:'Illustrative project CAPEX', file:'/data/ubon-cold-storage.csv' },
  { id:'02', tag:'F&B / SME FINANCE', title:'Mango Bomb — มะม่วงระเบิด', desc:'Build the financial story behind an interactive dessert concept. Structure unit economics, test pricing and discover the sales volume required to break even.', level:'Intermediate', color:'orange', skills:['Cost structuring','CVP analysis','Contribution margin','Break-even'], metric:'฿69', metricLabel:'Illustrative selling price / set', file:'/data/mango-bomb.csv' },
  { id:'03', tag:'MARKET FEASIBILITY', title:'Silver Economy: Elderly Care Hub', desc:'Translate demographic shifts into a market opportunity. Explore serviceable demand, customer segments and a data-led expansion case for elderly care.', level:'Advanced', color:'violet', skills:['Market sizing','Demographic analysis','Feasibility study','Data visualization'], metric:'20.0%', metricLabel:'Illustrative annual growth assumption', file:'/data/silver-economy.csv' }
]
const templates = [
  {name:'Loan Amortization Schedule',type:'Excel-ready CSV',desc:'Track principal, interest and outstanding balance by payment period.',file:'/templates/amortization-schedule.csv',icon:'calendar'},
  {name:'5-Year Financial Projection',type:'Excel-ready CSV',desc:'A clean operating model layout for revenue, costs, EBITDA and cash flow.',file:'/templates/5-year-projection.csv',icon:'chart'},
  {name:'Sensitivity Analysis',type:'Excel-ready CSV',desc:'Stress-test project value across discount-rate and growth assumptions.',file:'/templates/sensitivity-analysis.csv',icon:'grid'}
]
function App(){
 const [toast,setToast]=useState('')
 const [mobileOpen,setMobileOpen]=useState(false)
 const notify=(message)=>{setToast(message);window.clearTimeout(window.__fspToast);window.__fspToast=window.setTimeout(()=>setToast(''),2800)}
 const download=(file,name)=>{const a=document.createElement('a');a.href=file;a.download=name;a.click();notify('Your download is ready.')}
 const scrollTo=(id)=>{document.getElementById(id)?.scrollIntoView({behavior:'smooth'});setMobileOpen(false)}
 return <div className="min-h-screen bg-ink text-slate-100">
  <div className="top-glow" />
  <header className="nav-wrap"><nav className="container nav">
   <a href="#" className="brand" aria-label="Finance Sandbox Pro home"><span className="brand-mark"><BarChart3 size={19}/></span><span>finance<span className="brand-light">sandbox</span><b>pro.</b></span></a>
   <div className="nav-links"><button onClick={()=>scrollTo('work')}>Case studies</button><button onClick={()=>scrollTo('toolkit')}>Toolkits</button><a href="https://github.com/teanchai42752-cmyk/hadhed" target="_blank" rel="noreferrer">GitHub <ArrowUpRight size={13}/></a></div>
   <button className="nav-cta" onClick={()=>scrollTo('work')}>Explore projects <ArrowUpRight size={15}/></button>
   <button className="mobile-toggle" onClick={()=>setMobileOpen(!mobileOpen)} aria-label="Toggle menu">{mobileOpen?<X/>:<Menu/>}</button>
  </nav>{mobileOpen&&<div className="mobile-menu"><button onClick={()=>scrollTo('work')}>Case studies</button><button onClick={()=>scrollTo('toolkit')}>Toolkits</button><a href="https://github.com/teanchai42752-cmyk/hadhed">GitHub</a></div>}</header>
  <main>
   <section className="hero container">
    <div className="hero-copy"><div className="eyebrow"><span className="pulse"/> A PRACTICAL FINANCE PORTFOLIO <span className="eyebrow-line"/></div>
     <h1>Bridge the gap between<br/><span className="gradient-text">theory & real-world</span><br/>finance.</h1>
     <p className="hero-sub">Master messy data, build real valuation models, and prepare your portfolio for top-tier Corporate Finance and Advisory roles.</p>
     <div className="hero-actions"><button className="primary-btn" onClick={()=>scrollTo('work')}>Explore case studies <ArrowUpRight size={17}/></button><a className="text-link" href="#toolkit">Browse financial toolkits <ArrowDownRight size={16}/></a></div>
     <div className="hero-proof"><div className="avatar-stack"><span>CF</span><span>FP</span><span>DA</span></div><span>Built around practical finance workflows</span><span className="proof-dot">·</span><span className="mono">2026 EDITION</span></div>
    </div>
    <div className="hero-visual"><div className="visual-orbit orbit-one"/><div className="visual-orbit orbit-two"/><div className="dashboard-card">
      <div className="dash-head"><div><span className="dash-label">PORTFOLIO SNAPSHOT</span><div className="dash-title">Investment overview</div></div><span className="live-pill"><i/> LIVE MODEL</span></div>
      <div className="dash-value"><span>Enterprise value</span><strong>฿128.6<span>M</span></strong><small><ArrowUpRight size={13}/> +12.8% <em>vs. base case</em></small></div>
      <div className="chart-area"><div className="chart-y"><span>150</span><span>100</span><span>50</span><span>0</span></div><svg viewBox="0 0 430 150" preserveAspectRatio="none" role="img" aria-label="Illustrative valuation trend chart"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="#6ee7b7" stopOpacity=".24"/><stop offset="100%" stopColor="#6ee7b7" stopOpacity="0"/></linearGradient></defs><path d="M0 120 C30 112 38 118 65 96 S100 104 130 80 S164 89 195 67 S230 74 260 51 S300 62 330 35 S380 42 430 10 L430 150 L0 150Z" fill="url(#area)"/><path d="M0 120 C30 112 38 118 65 96 S100 104 130 80 S164 89 195 67 S230 74 260 51 S300 62 330 35 S380 42 430 10" fill="none" stroke="#6ee7b7" strokeWidth="2.5" strokeLinecap="round"/></svg></div>
      <div className="chart-months"><span>JAN</span><span>FEB</span><span>MAR</span><span>APR</span><span>MAY</span><span>JUN</span></div>
      <div className="dash-bottom"><div><span>WACC</span><b>9.40%</b></div><div><span>PROJECT IRR</span><b className="mint">16.2%</b></div><div><span>NPV</span><b>฿18.4M</b></div></div>
     </div><div className="float-chip chip-top"><span className="chip-icon"><Database size={15}/></span><div><b>Raw data</b><small>Clean. Model. Decide.</small></div><Check size={15} className="chip-check"/></div><div className="float-chip chip-bottom"><span className="chip-icon purple"><Zap size={15}/></span><div><b>Decision-ready</b><small>Finance meets execution</small></div></div><div className="visual-caption"><span className="caption-square"/> A BETTER WAY TO LEARN FINANCE</div>
    </div>
   </section>
   <section className="ticker"><div className="ticker-inner"><span>VALUATION</span><i/> <span>FINANCIAL MODELING</span><i/> <span>MARKET FEASIBILITY</span><i/> <span>DATA ANALYTICS</span><i/> <span>INVESTMENT THINKING</span><i/> <span>VALUATION</span></div></section>
   <section className="section container" id="work"><div className="section-head"><div><div className="eyebrow">01 / THE WORK</div><h2>Case studies<span className="muted-period">.</span></h2><p className="section-desc">Real-world inspired projects. Messy inputs. Clear financial decisions.</p></div><div className="section-aside"><span className="mono">SELECTED PROJECTS</span><span>01 — 03</span></div></div>
    <div className="case-grid">{cases.map(c=><article className={'case-card '+c.color} key={c.id}><div className="case-top"><span className="case-number">{c.id} / CASE STUDY</span><span className="level">{c.level}</span></div><div className="case-art"><div className="art-grid"/><div className="art-orb"/><span className="art-code">{c.id==='01'?'PROJECT / 2026':c.id==='02'?'UNIT ECONOMICS':'MARKET / THAILAND'}</span><div className="art-metric"><strong>{c.metric}</strong><span>{c.metricLabel}</span></div><div className="art-bars"><i/><i/><i/><i/><i/><i/><i/><i/><i/></div></div><div className="case-body"><span className="case-tag">{c.tag}</span><h3>{c.title}</h3><p>{c.desc}</p><div className="skills">{c.skills.map(s=><span key={s}>{s}</span>)}</div><button className="download-link" onClick={()=>download(c.file,c.file.split('/').pop())}><Download size={15}/> Download raw data <ArrowUpRight size={14}/></button></div></article>)}</div>
   </section>
   <section className="toolkit-section" id="toolkit"><div className="container section"><div className="section-head"><div><div className="eyebrow">02 / THE TOOLKIT</div><h2>Build with a head start<span className="muted-period">.</span></h2><p className="section-desc">Practical spreadsheet foundations. Download, customize and make them yours.</p></div><div className="toolkit-stamp"><FileSpreadsheet size={20}/><span>FREE RESOURCES<br/><b>OPEN FORMAT</b></span></div></div>
    <div className="toolkit-list">{templates.map((t,i)=><div className="toolkit-row" key={t.name}><div className="toolkit-index">0{i+1}</div><div className="toolkit-icon"><FileSpreadsheet size={20}/></div><div className="toolkit-info"><h3>{t.name}</h3><p>{t.desc}</p></div><span className="file-type">{t.type}</span><button className="icon-download" onClick={()=>download(t.file,t.file.split('/').pop())} aria-label={'Download '+t.name}><Download size={17}/></button></div>)}</div>
   </div></section>
   <section className="cta-section container"><div className="cta-card"><div className="cta-glow"/><div className="cta-content"><div className="eyebrow"><Sparkles size={13}/> KEEP BUILDING</div><h2>Make your next model<br/><span className="gradient-text">mean something.</span></h2><p>Good finance is more than formulas. It is the confidence to turn numbers into decisions.</p><button className="primary-btn" onClick={()=>scrollTo('work')}>Start exploring <ArrowRight size={16}/></button></div><div className="cta-side"><div className="big-bracket">{'{ }'}</div><span>THINK CLEAR.<br/>MODEL BETTER.</span></div></div></section>
  </main>
  <footer className="footer"><div className="container footer-inner"><a href="#" className="brand"><span className="brand-mark"><BarChart3 size={18}/></span><span>finance<span className="brand-light">sandbox</span><b>pro.</b></span></a><span className="footer-note">Independent learning project · Illustrative data for educational use</span><a className="footer-github" href="https://github.com/teanchai42752-cmyk/hadhed" target="_blank" rel="noreferrer"><Github size={15}/> View source <ArrowUpRight size={13}/></a><span className="copyright">© 2026 Finance Sandbox Pro</span></div></footer>
  {toast&&<div className="toast"><span><Check size={15}/></span>{toast}</div>}
 </div>
}
export default App