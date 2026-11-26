# Music + SFX for the "English, explained" template. Reads texts/timings from episode.js; scene timing matches index.html (T).
import json, re, numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, pyloudnorm as pyln
EP=json.loads(re.search(r'window\.EP\s*=\s*(\{.*\});',open('episode.js',encoding='utf-8').read(),re.S).group(1))
T=dict(dive=3.0,diveEnd=3.8,strike=4.2,cross=4.8,why=6.0,right=12.3,hl=14.0,stamp=15.0,ex=19.2,quiz=28.8,end=34.2)
SR=48000; DUR=EP['dur']; N=int(SR*DUR); BEAT=0.6
rng=np.random.default_rng(3); music=np.zeros((N,2)); sfx=np.zeros((N,2))
def add(bus,sig,t,g=1.0,pan=0.0):
    i=int(t*SR)
    if i>=N or i<0: return
    s=sig[:N-i]*g; l=np.cos((pan+1)*np.pi/4)*1.41; r=np.sin((pan+1)*np.pi/4)*1.41
    bus[i:i+len(s),0]+=s*l; bus[i:i+len(s),1]+=s*r
hz=lambda m:440*2**((m-69)/12)
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def noise(d): return rng.uniform(-1,1,int(d*SR))
def bp(x,lo,hi): return ss.lfilter(*ss.butter(2,[lo/(SR/2),hi/(SR/2)],'band'),x)
def lp(x,f): return ss.lfilter(*ss.butter(2,f/(SR/2)),x)
def hp(x,f): return ss.lfilter(*ss.butter(2,f/(SR/2),'high'),x)
def marimba(m,d=0.9,g=1):
    n=int(d*SR);t=np.arange(n)/SR;f=hz(m)
    return (np.sin(2*np.pi*f*t)*np.exp(-t/0.35)+0.35*np.sin(2*np.pi*f*4*t)*np.exp(-t/0.05)+0.15*np.sin(2*np.pi*f*10*t)*np.exp(-t/0.015))*env(n,.002,10)*g
def pizz(m,d=0.5):
    n=int(d*SR);t=np.arange(n)/SR;f=hz(m);x=sum(np.sin(2*np.pi*f*k*t)/k**1.3 for k in range(1,7))
    return lp(x,2500)*np.exp(-t/0.14)*env(n,.003,10)
def kick(): n=int(.35*SR);t=np.arange(n)/SR;f=55*(1+2.5*np.exp(-t*35));return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.16)
def brush(): return hp(noise(.25),1800)*env(int(.25*SR),.01,.07)*.5
def hat(): return hp(noise(.05),7000)*env(int(.05*SR),.001,.012)*.4
# ---- groove: F major, I-vi-IV-V, 100 BPM
prog=[(53,[65,69,72]),(50,[62,65,69]),(46,[58,62,65]),(48,[60,64,67])]  # F, Dm, Bb, C
def groove(a,b,level=1.0,full=True):
    bar=BEAT*4;k=int(round(a/bar))
    t=a
    while t<b-0.01:
        root,ch=prog[int(round(t/bar))%4]
        add(music,pizz(root-12,0.6),t,0.5*level); add(music,pizz(root-12,0.4),t+BEAT*2,0.35*level)
        for j,bt in enumerate([0.5,1.5,2.5,3.5]):
            add(music,pizz(ch[j%3],0.35),t+bt*BEAT,0.18*level,pan=-.3+.2*j)
        if full:
            for bt in [0,2]: add(music,kick(),t+bt*BEAT,0.55*level)
            for bt in [1,3]: add(music,brush(),t+bt*BEAT,0.5*level,.1)
            for bt in np.arange(0,4,.5): add(music,hat(),t+bt*BEAT,0.35*level,.3)
        t+=bar
mot=[(0,72),(.5,74),(1,77),(2,76),(2.5,74),(3,72)]
def motif(t0,g=.32,tr=0):
    for bt,m in mot: add(music,marimba(m+tr),t0+bt*BEAT,g,.25)
groove(0.0,2.4,0.55,full=False); groove(3.6,28.8,1.0)
motif(6.0);motif(8.4,tr=-2);motif(15.0,.36);motif(19.8,.3);motif(22.2,.3,tr=-2)
groove(28.8,34.2,0.6,full=False)  # quiz: lighter, suspense
for k,tt in enumerate(np.arange(30.0,34.2,BEAT/2)): add(music,marimba(84 if k%2==0 else 79,.25),tt,.08,.4)  # tick-tock
for m,dl in [(65,0),(69,.03),(72,.06),(77,.09)]: add(music,marimba(m,1.6),34.8+dl,.35)
groove(34.8,36.0,.8)
# ---- SFX
def pop(f0=700,g=.4): n=int(.09*SR);t=np.arange(n)/SR;f=f0*(1+1.2*np.exp(-t*60));return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.03)*g
def tap(): return hp(noise(.02),2500)*env(int(.02*SR),.0005,.004)*.5
def whoosh(d=.7,g=.4):
    n=int(d*SR);x=noise(d);y=np.zeros(n)
    for s in range(10):
        a=s*n//10;b=(s+1)*n//10;f=400+3500*np.sin(np.pi*a/n);y[a:b]=bp(x,f*.6,min(20000,f*1.6))[a:b]
    return y*np.sin(np.pi*np.linspace(0,1,n))**1.5*g
def scratch(d,g=.25):
    n=int(d*SR);x=bp(noise(d),1800,6500);m=(0.55+0.45*np.sign(np.sin(2*np.pi*np.cumsum(9+5*rng.random(n))/SR)))
    return x*m*np.minimum(1,np.arange(n)/(.01*SR))*np.minimum(1,(n-np.arange(n))/(.02*SR))*g
def buzzer(): n=int(.35*SR);t=np.arange(n)/SR;x=ss.square(2*np.pi*140*t)*.5+ss.square(2*np.pi*147*t)*.5;return lp(x,1800)*env(n,.005,.2)*.35
def ding(): n=int(1.4*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1568*t)+.5*np.sin(2*np.pi*2349*t)+.25*np.sin(2*np.pi*3136*t))*np.exp(-t/.45)*env(n,.002,9)*.25
def thump(): n=int(.3*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*90*t)*np.exp(-t/.06)+lp(noise(.3),900)*np.exp(-t/.03)*.6)*.7
def slap(): return (lp(noise(.12),2500)*env(int(.12*SR),.001,.03)+hp(noise(.12),3000)*env(int(.12*SR),.0005,.01)*.4)*.8
def swipe(d=.7): n=int(d*SR);return bp(noise(d),900,4000)*np.sin(np.pi*np.linspace(0,1,n))*.18
def measure_w(text,px): return len(text)*px*0.5
# chat
for m in EP['chat']['msgs']:
    if 'typing' in m:
        for tt in np.arange(m['typing'][0],m['typing'][1],.11): add(sfx,tap(),tt+.02*rng.random(),.6,.2)
    else: add(sfx,pop(820 if m['from']=='me' else 600),m['t'],.9,.3 if m['from']=='me' else -.3)
add(sfx,whoosh(.9,.45),T['dive']-.1)
add(sfx,scratch(.38,.3),T['strike']); add(sfx,buzzer(),T['strike']+.05)
add(sfx,pop(420,.35),T['cross'])
def wdur(text,px=74): return min(1.5,max(.55,len(text)*px*0.42/650))
for n in EP['why']: add(sfx,scratch(wdur(n['text']),.22),n['t'],1,-.1)
add(sfx,whoosh(.6,.3),11.6)
add(sfx,scratch(wdur(EP['right']['text'],80),.22),T['right'])
add(sfx,swipe(),T['hl']); add(sfx,thump(),T['stamp']); add(sfx,ding(),T['stamp']+.04)
add(sfx,whoosh(.7,.35),18.9)
for e in EP['examples']: add(sfx,slap(),e['t'],1,-.2)
add(sfx,scratch(wdur(EP['note']['text']),.22),EP['note']['t'])
add(sfx,whoosh(.6,.35),T['quiz']-.1)
for k,dt in enumerate([.35,.95,1.55]): add(sfx,pop(600,.35),T['quiz']+dt,.9,-.3)
add(sfx,pop(900,.35),T['quiz']+2.2)
add(sfx,whoosh(.7,.35),T['end']); add(sfx,slap(),T['end']+.4); add(sfx,thump(),T['end']+1.0); add(sfx,ding(),T['end']+1.04)
# episode-specific touches
if 'ghost' in EP['wrong']: add(sfx,whoosh(.5,.18),EP['wrong']['ghostT'])          # the silent h fades
if 'clock' in EP:
    c=EP['clock']['t']; add(sfx,scratch(.55,.2),c)
    for k in range(4): add(sfx,tap(),c+.6+k*.15,1.4,-.3)                          # clock ticks
for e in EP['examples']:
    if 'sub' in e: add(sfx,scratch(.6,.15),e['t']+.45,1,.1)
# ---- mix
fade=np.ones(N);fl=int(.4*SR);fade[-fl:]=np.linspace(1,0,fl)**2
def fin(m,s,mg,sg,target=None,gain=None):
    x=(m*mg+s*sg)*fade[:,None];x=ss.lfilter(*ss.butter(1,30/(SR/2),'high'),x,axis=0);M=pyln.Meter(SR)
    if gain is None: gain=10**((target-M.integrated_loudness(x))/20)
    x=x*gain
    if np.max(np.abs(x))>.89: x=np.tanh(x/.89)*.89
    return x,gain,M.integrated_loudness(x)
full,g,L=fin(music,sfx,1,.9,target=-14); bed,_,L2=fin(music,sfx,.28,.55,gain=g)
print('full %.1f LUFS pk %.2f | bed %.1f'%(L,np.max(np.abs(full)),L2))
wf.write('mix_full.wav',SR,(full*32767).astype(np.int16)); wf.write('mix_voicebed.wav',SR,(bed*32767).astype(np.int16))
