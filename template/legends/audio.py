import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, pyloudnorm as pyln
SR=48000; DUR=37.2; N=int(SR*DUR); BEAT=0.6
rng=np.random.default_rng(7)
music=np.zeros((N,2)); sfx=np.zeros((N,2))
def add(bus,sig,t,gain=1.0,pan=0.0):
    i=int(t*SR);
    if i>=N: return
    s=sig[:N-i]*gain; l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    bus[i:i+len(s),0]+=s*l*1.41; bus[i:i+len(s),1]+=s*r*1.41
def hz(m): return 440*2**((m-69)/12)
def ks(f,dur=1.6,bright=0.6,damp=0.996):  # Karplus-Strong pluck (dombra-like)
    n=int(dur*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p)
    buf=ss.lfilter([bright,1-bright],[1],buf) if bright<1 else buf
    out=np.zeros(n); b=buf.copy(); idx=0
    for k in range(n):
        v=b[idx]; nxt=b[(idx+1)%p]; b[idx]=damp*0.5*(v+nxt); out[k]=v; idx=(idx+1)%p
    # body resonance + attack click
    out=ss.lfilter(*ss.butter(2,[180/(SR/2),3800/(SR/2)],'band'),out)*1.6+out*0.4
    env=np.minimum(1,np.arange(n)/(0.002*SR)); return out*env
cache={}
def pluck(m,dur=1.4,bright=0.55):
    k=(m,dur,bright)
    if k not in cache: cache[k]=ks(hz(m),dur,bright)
    return cache[k]
def noise(d): return rng.uniform(-1,1,int(d*SR))
def bp(x,lo,hi,o=2): return ss.lfilter(*ss.butter(o,[lo/(SR/2),hi/(SR/2)],'band'),x)
def lp(x,f,o=2): return ss.lfilter(*ss.butter(o,f/(SR/2)),x)
def hp(x,f,o=2): return ss.lfilter(*ss.butter(o,f/(SR/2),'high'),x)
def envAD(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def drum(gain=1,f0=95,d=0.35):
    n=int(0.9*SR); t=np.arange(n)/SR; f=f0*(1+1.2*np.exp(-t*30)); ph=2*np.pi*np.cumsum(f)/SR
    body=np.sin(ph)*np.exp(-t/d); skin=bp(noise(0.9),300,2500)*np.exp(-t/0.04)*0.35
    return (body+skin)*gain
D3,F3,G3,A3,C4,D4,E4,F4,Fs4,G4,A4,B4,C5,D5=50,53,55,57,60,62,64,65,66,67,69,71,72,74
# ---------- strum pattern (dombra "катпа" feel) ----------
def strum(t,root=D3,fifth=G3,vel=1.0,up=False):
    for j,m in enumerate([root,fifth] if not up else [fifth,root]):
        add(music,pluck(m,1.2,0.5),t+j*0.012,0.22*vel,pan=-0.25+0.5*j)
def strum_section(a,b,vel,root=D3,fifth=A3):
    t=a
    while t<b-0.01:
        strum(t,root,fifth,vel); strum(t+BEAT*0.5,root,fifth,vel*0.55,up=True); strum(t+BEAT*0.75,root,fifth,vel*0.7)
        t+=BEAT
# hook (0-3)
for tt,m,g in [(0.08,D4,.5),(0.32,A4,.8),(0.6,G4,.55),(0.9,F4,.45),(1.25,D4,.5),(1.55,C4,.4),(1.85,D4,.55)]:
    add(music,pluck(m+12 if m<60 else m,1.6,0.7),tt,g*0.55,0.15)
add(music,drum(1.0,85,0.45),0.32,0.9); add(music,drum(.6,110,.25),1.25,0.5)
strum_section(1.8,3.0,0.55)
# story A (3-18): strum + melody
strum_section(3.0,18.0,0.75)
mel=[(0,D5),(1,C5),(1.5,A4),(2,G4),(3,A4),(4,C5),(5,A4),(5.5,G4),(6,F4),(7,D4)]
for rep_start in [3.0+BEAT*4*0,3.0+BEAT*8,3.0+BEAT*16]:
    for bt,m in mel: add(music,pluck(m,1.4,0.65),rep_start+bt*BEAT,0.32,0.3)
# drone
t=np.arange(N)/SR
drone=(np.sin(2*np.pi*hz(38)*t)+0.4*np.sin(2*np.pi*hz(45)*t))*0.05
dmask=np.clip((t-3.0)/1.0,0,1)*np.clip((24.0-t)/0.2,0,1)
music[:,0]+=drone*dmask; music[:,1]+=drone*dmask
for b in np.arange(3.0,18.0,BEAT*4): add(music,drum(0.55,90,0.3),b,0.6)
# tension (18-24): tremolo rising, heartbeat
for k,tt in enumerate(np.arange(18.0,24.0,BEAT/4)):
    prog=(tt-18)/6; m=[A4,A4,C5,C5,D5,D5][int(prog*6)]
    add(music,pluck(m,0.5,0.8),tt,0.08+0.17*prog,0.35)
for tt in np.arange(18.0,24.0,BEAT):
    add(music,drum(0.5,70,0.2),tt,0.35+0.3*(tt-18)/6); add(music,drum(0.35,70,0.15),tt+0.18,0.25)
# riser
n=int(1.4*SR); r=bp(noise(1.4),800,6000)*np.linspace(0,1,n)**2*0.12; add(music,r,22.6,1.0)
# sunrise (24-28.8): bright D major
add(music,drum(1.4,70,0.6),24.0,1.0)
for m,dl in [(D3,0),(A3,.01),(D4,.02),(Fs4,.03),(A4,.04),(D5,.05)]: add(music,pluck(m,2.5,0.75),24.0+dl,0.32)
strum_section(24.6,32.4,0.8,root=D3,fifth=A3)
mel2=[(0,Fs4),(0.5,A4),(1,B4),(2,A4),(3,D5),(4,B4),(4.5,A4),(5,Fs4),(6,E4),(7,D4)]
for rs in [24.6,24.6+BEAT*8]:
    for bt,m in mel2: add(music,pluck(m,1.4,0.7),rs+bt*BEAT,0.34,0.3)
for b in np.arange(24.0,32.4,BEAT*2): add(music,drum(0.7,85,0.3),b,0.6)
# camel in ash (32.4-34.8): comic descending
for k,(bt,m) in enumerate([(0,A4),(0.5,G4),(1,F4),(1.5,E4),(2,D4),(3,A3)]):
    add(music,pluck(m,1.0,0.5),32.4+bt*BEAT,0.35,-0.2)
add(music,drum(0.6,60,0.4),33.6,0.6)
# end card (34.8-37.2)
strum_section(34.8,36.0,0.8,root=D3,fifth=A3)
for m,dl in [(D3,0),(A3,.015),(D4,.03),(Fs4,.045),(A4,.06),(D5,.075)]: add(music,pluck(m,1.3,0.75),36.0+dl,0.3)
add(music,drum(1.0,80,0.5),36.0,0.8)
# ---------- SFX ----------
def whoosh(d=0.45,lo=400,hi=3500,g=0.35):
    n=int(d*SR); x=noise(d); sweep=np.linspace(0,1,n)
    y=np.zeros(n);
    for seg in range(8):
        a=seg*n//8; b=(seg+1)*n//8; f=lo+(hi-lo)*np.sin(np.pi*(a/n))
        y[a:b]=bp(x,max(80,f*0.6),min(18000,f*1.6))[a:b]
    env=np.sin(np.pi*sweep)**1.5; return y*env*g
def snap(g=0.5):
    x=hp(noise(0.05),2500)*envAD(int(0.05*SR),0.0005,0.012); n=int(0.12*SR); tt=np.arange(n)/SR
    blip=np.sin(2*np.pi*(900+700*np.exp(-tt*30))*tt)*np.exp(-tt/0.04)*0.4
    y=np.zeros(n); y[:len(x)]+=x; y+=blip; return y*g
def tick(g=0.2,f=3000):
    n=int(0.03*SR); return hp(noise(0.03),f)*envAD(n,0.0003,0.006)*g
def squeak(g=0.25,f0=2400,f1=3600,d=0.09):
    n=int(d*SR); tt=np.arange(n)/SR; f=np.linspace(f0,f1,n)+80*np.sin(2*np.pi*40*tt)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tt/d)*g
def grumble(g=0.35,d=0.7):
    n=int(d*SR); tt=np.arange(n)/SR; f=95*(1+0.08*np.sin(2*np.pi*7*tt))*np.linspace(1.05,0.85,n)
    saw=ss.sawtooth(2*np.pi*np.cumsum(f)/SR); y=bp(saw,150,900)+0.6*bp(saw,500,1300)
    return y*np.sin(np.pi*tt/d)**0.7*g
def chime(m,g=0.2,d=2.0):
    n=int(d*SR); tt=np.arange(n)/SR; f=hz(m)
    return sum(np.sin(2*np.pi*f*k*tt)*np.exp(-tt/(d/(k*0.8)))*a for k,a in [(1,1),(2.76,.4),(5.4,.2)])*envAD(n,0.002,d)*g
def puff(g=0.3):
    d=0.4; n=int(d*SR); return lp(noise(d),600)*envAD(n,0.01,0.12)*g
for tt,d,gg,pan in [(2.95,0.9,0.4,0),(8.35,0.5,0.3,-0.3),(13.15,0.7,0.35,0.2),(17.95,0.55,0.3,-0.2),(23.85,0.7,0.45,0.3),(28.75,0.9,0.4,0),(32.35,0.7,0.35,0)]:
    add(sfx,whoosh(d,300,4000,gg),tt-0.1,1,pan)
for tt in [9.6,14.4,25.8,29.4]: add(sfx,snap(0.55),tt+0.02,1,-0.3)
for tt in [3.2,8.6,13.4,18.2,21.0,25.4,29.0,32.6]: add(sfx,tick(0.18,2000),tt+0.18,1,0.2)
for tt in [0.08,0.6,1.25]: add(sfx,tick(0.3,1500),tt,1)
add(sfx,snap(0.6),0.32,1)
add(sfx,squeak(0.22),8.75,1,-0.2); add(sfx,squeak(0.18,2600,3300,0.07),8.9,1,-0.2)
add(sfx,grumble(0.32),13.5,1,0.2)
for tt in np.arange(18.6,23.3,0.085):
    add(sfx,tick(0.10+0.04*rng.random(),3500+2000*rng.random()),tt+0.01*rng.random(),1,-0.1+0.2*rng.random())
add(sfx,squeak(0.3,2400,4200,0.14),24.02,1,0.2); add(sfx,squeak(0.25,3000,4400,0.1),24.2,1,0.2)
for k,m in enumerate([D5+12,A4+12,Fs4+12,D5+24]): add(sfx,chime(m,0.08,2.5),24.0+k*0.09,1,0.4-0.25*k)
add(sfx,chime(D5+12,0.12,1.8),30.35,1,0); add(sfx,chime(A4+12,0.08,1.6),30.45,1,0)
for k in range(14): add(sfx,puff(0.28),33.0+k*0.17,1,-0.4+0.06*k)
add(sfx,grumble(0.22,0.9),33.2,1,0)
for tt in [35.1,35.4,35.7,36.0]: add(sfx,tick(0.22,1800),tt,1)
add(sfx,snap(0.45),36.3,1)
# ---------- mix ----------
fade=np.ones(N); fl=int(0.5*SR); fade[-fl:]=np.linspace(1,0,fl)**2
def finalize(m,s,mg,sg,target=None,gain=None):
    x=(m*mg+s*sg)*fade[:,None]
    x=ss.lfilter(*ss.butter(1,30/(SR/2),'high'),x,axis=0)
    meter=pyln.Meter(SR)
    if gain is None: gain=10**((target-meter.integrated_loudness(x))/20)
    x=x*gain; pk=np.max(np.abs(x))
    if pk>0.89: x=np.tanh(x/0.89*1.0)*0.89  # soft limit
    return x,gain,meter.integrated_loudness(x)
full,g,L=finalize(music,sfx,1.0,0.9,target=-14)
bed,_,L2=finalize(music,sfx,0.28,0.5,gain=g)
print('full LUFS %.1f peak %.2f | bed LUFS %.1f peak %.2f'%(L,np.max(np.abs(full)),L2,np.max(np.abs(bed))))
wf.write('mix_full.wav',SR,(full*32767).astype(np.int16)); wf.write('mix_voicebed.wav',SR,(bed*32767).astype(np.int16))
