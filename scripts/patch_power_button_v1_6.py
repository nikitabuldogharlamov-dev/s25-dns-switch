from pathlib import Path

root = Path('S25-DNS-Switch')
p = root / 'app/src/main/java/com/s25/dnstile/MainActivity.java'
s = p.read_text(encoding='utf-8')
old = '''            paint.setStrokeWidth(dp(8));
            paint.setShader(new SweepGradient(cx,cy,new int[]{BLUE,VIOLET,BLUE},null));
            paint.setShadowLayer(on ? dp(17) : dp(6),0,0,on ? VIOLET : OUTLINE);
            canvas.drawCircle(cx,cy,radius,paint);
            paint.clearShadowLayer(); paint.setShader(null);
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(CARD);
            canvas.drawCircle(cx,cy,radius-dp(6),paint);
            paint.setColor(on ? WHITE : SECOND);'''
new = '''            paint.setStrokeWidth(dp(on ? 8 : 6));
            if (on) {
                // Vibrant blue-violet ring with a visible halo only while DNS is enabled.
                paint.setShader(new SweepGradient(cx,cy,new int[]{BLUE,VIOLET,BLUE},null));
                paint.setShadowLayer(dp(20),0,0,VIOLET);
            } else {
                // Fully neutral, matte grey: no gradient, glow or shadow when disabled.
                paint.setShader(null);
                paint.clearShadowLayer();
                paint.setColor(Color.rgb(76, 87, 106));
            }
            canvas.drawCircle(cx,cy,radius,paint);
            paint.clearShadowLayer(); paint.setShader(null);
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(on ? Color.rgb(23, 26, 47) : CARD);
            canvas.drawCircle(cx,cy,radius-dp(6),paint);
            paint.setColor(on ? WHITE : Color.rgb(109, 121, 143));'''
if s.count(old) != 1:
    raise SystemExit(f'Expected PowerOrb code exactly once, found {s.count(old)}')
s = s.replace(old,new)
old_status='TextView status = text(enabled ? "Активен" : "Автоматический DNS", 24, WHITE, true);'
new_status='TextView status = text(enabled ? "Активен" : "Автоматический DNS", 24, enabled ? WHITE : SECOND, true);'
if s.count(old_status)!=1: raise SystemExit('Expected status label not found')
s = s.replace(old_status,new_status)
s = s.replace('DNS Switch 1.5. Dark UI;', 'DNS Switch 1.6. Dark UI;')
s = s.replace('Версия 1.5 • Samsung One UI','Версия 1.6 • Samsung One UI')
p.write_text(s,encoding='utf-8')

build = root / 'app/build.gradle'
cfg=build.read_text(encoding='utf-8')
assert 'versionCode 6' in cfg and "versionName '1.5 UI'" in cfg
cfg=cfg.replace('versionCode 6','versionCode 7').replace("versionName '1.5 UI'","versionName '1.6 Glow'")
build.write_text(cfg,encoding='utf-8')
print('Power button: ON glowing violet-blue; OFF fully matte grey; version 1.6')
