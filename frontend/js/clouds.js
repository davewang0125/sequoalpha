// Wallpaper Engine-style animated background
// WebGL shader: cloud flow + god rays + floating particles + light breathing
(function() {
  'use strict';

  const VERTEX_SRC = `
    attribute vec2 aPosition;
    varying vec2 vUv;
    void main() {
      vUv = aPosition * 0.5 + 0.5;
      gl_Position = vec4(aPosition, 0.0, 1.0);
    }
  `;

  const FRAGMENT_SRC = `
    precision mediump float;
    varying vec2 vUv;
    uniform sampler2D uImage;
    uniform float uTime;
    uniform vec2 uResolution;

    // ---- Simplex 2D noise ----
    vec3 mod289(vec3 x) { return x - floor(x * (1.0/289.0)) * 289.0; }
    vec2 mod289(vec2 x) { return x - floor(x * (1.0/289.0)) * 289.0; }
    vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

    float snoise(vec2 v) {
      const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                         -0.577350269189626, 0.024390243902439);
      vec2 i  = floor(v + dot(v, C.yy));
      vec2 x0 = v - i + dot(i, C.xx);
      vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
      vec4 x12 = x0.xyxy + C.xxzz;
      x12.xy -= i1;
      i = mod289(i);
      vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
                                   + i.x + vec3(0.0, i1.x, 1.0));
      vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
                               dot(x12.zw,x12.zw)), 0.0);
      m = m*m; m = m*m;
      vec3 x = 2.0 * fract(p * C.www) - 1.0;
      vec3 h = abs(x) - 0.5;
      vec3 ox = floor(x + 0.5);
      vec3 a0 = x - ox;
      m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
      vec3 g;
      g.x = a0.x * x0.x + h.x * x0.y;
      g.yz = a0.yz * x12.xz + h.yz * x12.yw;
      return 130.0 * dot(m, g);
    }

    float fbm(vec2 p) {
      float f = 0.0;
      f += 0.5000 * snoise(p); p *= 2.02;
      f += 0.2500 * snoise(p); p *= 2.03;
      f += 0.1250 * snoise(p); p *= 2.01;
      f += 0.0625 * snoise(p);
      return f;
    }

    // ---- Hash for particles ----
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }

    void main() {
      vec2 uv = vUv;
      vec2 imgUv = vec2(uv.x, 1.0 - uv.y);

      // === 1. CLOUD FLOW ===
      vec4 origColor = texture2D(uImage, imgUv);
      float brightness = dot(origColor.rgb, vec3(0.299, 0.587, 0.114));

      // Cloud mask: only displace bright cloud pixels
      float cloudMask = smoothstep(0.45, 0.85, brightness);

      // Protect the tree area (center of image)
      float cx = abs(uv.x - 0.5);
      float cy = 1.0 - uv.y;
      float treeMask = 1.0 - smoothstep(0.08, 0.35, length(vec2(cx * 0.8, (cy - 0.35) * 1.2)));
      treeMask = max(treeMask, 0.0);
      cloudMask *= (1.0 - treeMask * 0.7);

      float t = uTime * 0.12;
      vec2 noiseCoord1 = uv * 2.5 + vec2(t, t * 0.3);
      vec2 noiseCoord2 = uv * 4.0 + vec2(t * 0.7 + 50.0, t * 0.2 + 30.0);

      float n1x = fbm(noiseCoord1);
      float n1y = fbm(noiseCoord1 + vec2(7.3, 2.8));
      float n2x = fbm(noiseCoord2);
      float n2y = fbm(noiseCoord2 + vec2(3.1, 8.4));

      vec2 displacement = vec2(
        n1x * 0.7 + n2x * 0.3,
        n1y * 0.5 + n2y * 0.2
      );

      float strength = cloudMask * 0.045;
      vec2 displaced = imgUv + displacement * strength;
      displaced = clamp(displaced, vec2(0.0), vec2(1.0));

      vec4 color = texture2D(uImage, displaced);


      // === 2. LIGHT BREATHING ===
      // Sun is at top-center of the image (uv.y near 1.0, uv.x near 0.5)
      vec2 sunPos = vec2(0.5, 0.92);
      float sunDist = length((uv - sunPos) * vec2(1.0, 1.4));

      // Gentle pulsing brightness near the sun
      float breathe = sin(uTime * 0.3) * 0.3 + sin(uTime * 0.17) * 0.2;
      float breatheMask = smoothstep(0.8, 0.0, sunDist) * 0.06;
      color.rgb += breatheMask * breathe;


      // Tree block mask (reused by particles)
      float treeBlock = smoothstep(0.12, 0.3, length(vec2((uv.x - 0.5) * 0.9, (uv.y - 0.55) * 1.5)));


      // === 3. FLOATING PARTICLES ===
      // Multiple particle layers for depth
      float particleAccum = 0.0;

      for (int layer = 0; layer < 3; layer++) {
        float fl = float(layer);
        float layerScale = 40.0 + fl * 25.0; // different grid sizes per layer
        float speed = 0.03 + fl * 0.015;      // different speeds
        float size = 0.012 - fl * 0.003;       // smaller particles further back
        float bright = 0.8 - fl * 0.2;         // dimmer further back

        // Particle grid - each cell may contain one particle
        vec2 particleUv = uv * layerScale;
        // Drift: particles float upward and slightly sideways
        particleUv.y -= uTime * speed;
        particleUv.x += sin(uTime * 0.1 + fl * 2.0) * 0.5;

        vec2 cellId = floor(particleUv);
        vec2 cellUv = fract(particleUv);

        // Random position within cell
        float rnd = hash(cellId + fl * 100.0);
        float rnd2 = hash(cellId + fl * 100.0 + vec2(37.0, 91.0));

        // Only ~30% of cells have a particle
        if (rnd > 0.7) {
          vec2 particlePos = vec2(
            hash(cellId + vec2(13.0, 7.0) + fl * 50.0),
            hash(cellId + vec2(43.0, 29.0) + fl * 50.0)
          );

          float d = length(cellUv - particlePos);
          // Soft glowing dot
          float particle = smoothstep(size, size * 0.1, d);

          // Twinkle
          float twinkle = sin(uTime * (1.5 + rnd * 2.0) + rnd2 * 6.28) * 0.5 + 0.5;
          twinkle = 0.4 + 0.6 * twinkle;

          // Particles more visible in brighter areas (sky/clouds)
          float visMask = smoothstep(0.3, 0.6, brightness);
          // Reduce in tree area
          visMask *= treeBlock;

          particleAccum += particle * twinkle * bright * visMask;
        }
      }

      // Warm white particles
      vec3 particleColor = vec3(1.0, 0.98, 0.9);
      color.rgb += particleColor * particleAccum * 0.35;


      // === 5. SUBTLE VIGNETTE ===
      float vignette = 1.0 - smoothstep(0.5, 1.4, length((uv - 0.5) * vec2(1.2, 1.0)));
      color.rgb *= 0.92 + 0.08 * vignette;


      gl_FragColor = color;
    }
  `;

  function createCloudCanvas(container) {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:0;';
    container.insertBefore(canvas, container.firstChild);

    const gl = canvas.getContext('webgl', { alpha: false, antialias: false });
    if (!gl) {
      console.warn('WebGL not available, falling back to static background');
      canvas.remove();
      return { destroy: () => {} };
    }

    function compileShader(type, src) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
        console.error('Shader error:', gl.getShaderInfoLog(s));
        return null;
      }
      return s;
    }

    const vs = compileShader(gl.VERTEX_SHADER, VERTEX_SRC);
    const fs = compileShader(gl.FRAGMENT_SHADER, FRAGMENT_SRC);
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);

    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(prog));
      canvas.remove();
      return { destroy: () => {} };
    }

    gl.useProgram(prog);

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
    const aPos = gl.getAttribLocation(prog, 'aPosition');
    gl.enableVertexAttribArray(aPos);
    gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

    const uTime = gl.getUniformLocation(prog, 'uTime');
    const uResolution = gl.getUniformLocation(prog, 'uResolution');
    const uImage = gl.getUniformLocation(prog, 'uImage');

    const tex = gl.createTexture();
    const img = new Image();
    img.crossOrigin = 'anonymous';
    let imageLoaded = false;
    img.onload = () => {
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      imageLoaded = true;
    };
    img.src = 'images/v1_21.png';

    let animId;
    let startTime = performance.now();

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.floor(container.offsetWidth * dpr);
      canvas.height = Math.floor(container.offsetHeight * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
    }

    function render(timestamp) {
      animId = requestAnimationFrame(render);
      if (!imageLoaded) return;

      const elapsed = (timestamp - startTime) / 1000.0;
      gl.uniform1f(uTime, elapsed);
      gl.uniform2f(uResolution, canvas.width, canvas.height);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.uniform1i(uImage, 0);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    resize();
    animId = requestAnimationFrame(render);

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 150);
    });

    return {
      destroy: () => {
        cancelAnimationFrame(animId);
        canvas.remove();
      }
    };
  }

  window.createCloudCanvas = createCloudCanvas;
})();
