import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Box,
  Camera,
  ClipboardCheck,
  Download,
  ExternalLink,
  FileText,
  Grid3X3,
  Layers,
  Maximize2,
  PackageSearch,
  Pause,
  Play,
  RotateCcw,
  RotateCw,
  ScanSearch,
  Target,
  View
} from "lucide-react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { modelData, type PackedMesh } from "./model-data";
import { downloads, groundImages, logoDataUri, viewerConfig } from "./generated-assets";

type ViewMode = "home" | "front" | "top" | "detail";
type SceneApi = {
  setView: (view: ViewMode) => void;
  reset: () => void;
  capture: () => void;
};

const companySlogan =
  viewerConfig.companySlogan || "Specialized in design and manufacturing SMT THT machine for smart EMS Factory";
const productTitle = viewerConfig.productTitle || "Product Interactive 3D Viewer";
const sourceNotice =
  viewerConfig.sourceNotice ||
  "This interactive 3D view helps engineers review product geometry, clearance, and integration concept before final compatibility confirmation.";

const defaultMarketingTiles = [
  {
    label: "Features",
    text: "3D STEP visual reference, gripper-style nozzle body, compact clamping area, and embedded CAD/PDF source files."
  },
  {
    label: "Advantages",
    text: "Makes geometry, clearance, and machine-interface discussions easier before engineering confirmation."
  },
  {
    label: "Benefits",
    text: "Reduces early design back-and-forth and helps speed up custom nozzle review for SMT production setup."
  },
  {
    label: "Applications",
    text: "Used for SMT pick-and-place handling of odd-form, connector, terminal, E-cap, and other non-standard components."
  }
];

const defaultRfqItems = [
  {
    label: "Machine model",
    text: "Exact production machine brand/model, head or station, and current part reference if available."
  },
  {
    label: "Detailed product drawing",
    text: "Dimensioned 2D/3D drawing of the target component, PCB, feeder, fixture, or process part."
  },
  {
    label: "Component samples or photos",
    text: "Clear photos, sample availability, weight, material, surface condition, and packaging direction."
  },
  {
    label: "Application requirement",
    text: "Target quantity, pickup problem, orientation requirement, and any clearance limits on the PCB."
  }
];

const marketingTiles = viewerConfig.marketingTiles || defaultMarketingTiles;
const rfqItems = viewerConfig.rfqItems || defaultRfqItems;
const rfqIntro =
  (viewerConfig as typeof viewerConfig & { rfqIntro?: string }).rfqIntro ||
  "For this product quotation, please provide these details first.";
const rfqIcons = [<Target size={16} />, <FileText size={16} />, <PackageSearch size={16} />, <ClipboardCheck size={16} />];

function makeDownload(asset: { name: string; mime: string; base64: string }) {
  const binary = atob(asset.base64);
  const chunks: Uint8Array[] = [];
  const chunkSize = 8192;
  for (let offset = 0; offset < binary.length; offset += chunkSize) {
    const slice = binary.slice(offset, offset + chunkSize);
    const bytes = new Uint8Array(slice.length);
    for (let i = 0; i < slice.length; i += 1) bytes[i] = slice.charCodeAt(i);
    chunks.push(bytes);
  }
  const url = URL.createObjectURL(new Blob(chunks, { type: asset.mime }));
  const link = document.createElement("a");
  link.href = url;
  link.download = asset.name;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1200);
}

function MarketingTiles() {
  return (
    <div className="stats-strip marketing-tiles" aria-label="Product sales highlights">
      {marketingTiles.map((item) => (
        <article className="marketing-tile" key={item.label}>
          <strong>{item.label}</strong>
          <span>{item.text}</span>
        </article>
      ))}
    </div>
  );
}

function ControlButton({
  active,
  icon,
  label,
  onClick
}: {
  active?: boolean;
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
}) {
  return (
    <button className={active ? "tool-button active" : "tool-button"} type="button" onClick={onClick}>
      {icon}
      <span>{label}</span>
    </button>
  );
}

function Viewer({
  autoRotate,
  wireframe,
  explode,
  showGrid,
  onApi
}: {
  autoRotate: boolean;
  wireframe: boolean;
  explode: number;
  showGrid: boolean;
  onApi: (api: SceneApi | null) => void;
}) {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const stateRef = useRef<{
    renderer: THREE.WebGLRenderer;
    camera: THREE.PerspectiveCamera;
    controls: OrbitControls;
    scene: THREE.Scene;
    modelGroup: THREE.Group;
    meshItems: Array<{ mesh: THREE.Mesh; direction: THREE.Vector3 }>;
    groundItems: Array<{ mesh: THREE.Mesh; material: THREE.MeshBasicMaterial; texture: THREE.Texture }>;
    grid: THREE.GridHelper;
    frame: number;
  } | null>(null);
  const flagsRef = useRef({ autoRotate, wireframe, explode, showGrid });

  useEffect(() => {
    flagsRef.current = { autoRotate, wireframe, explode, showGrid };
    const current = stateRef.current;
    if (!current) return;
    current.controls.autoRotate = autoRotate;
    current.grid.visible = showGrid;
    current.meshItems.forEach(({ mesh }) => {
      const material = mesh.material as THREE.MeshStandardMaterial;
      material.wireframe = wireframe;
      material.needsUpdate = true;
    });
  }, [autoRotate, wireframe, explode, showGrid]);

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return undefined;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f3ef);

    const camera = new THREE.PerspectiveCamera(38, 1, 0.01, 1000);
    camera.position.set(7.2, 4.6, 7.8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    host.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.07;
    controls.autoRotate = autoRotate;
    controls.autoRotateSpeed = 1.3;
    controls.enablePan = true;
    controls.minDistance = 2.2;
    controls.maxDistance = 18;

    const hemi = new THREE.HemisphereLight(0xffffff, 0x8c8172, 1.6);
    scene.add(hemi);

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.6);
    keyLight.position.set(4, 6, 5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0x78d6d2, 1.25);
    rimLight.position.set(-5, 3, -3);
    scene.add(rimLight);

    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(5.2, 96),
      new THREE.MeshStandardMaterial({ color: 0xe2ded4, roughness: 0.9, metalness: 0.02 })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -2.205;
    floor.receiveShadow = true;
    scene.add(floor);

    const groundItems: Array<{ mesh: THREE.Mesh; material: THREE.MeshBasicMaterial; texture: THREE.Texture }> = [];
    const textureLoader = new THREE.TextureLoader();
    const floorImageCount = Math.min(2, groundImages.length);
    if (floorImageCount > 0) {
      const panelWidth = floorImageCount === 1 ? 7.2 : 4.9;
      const panelDepth = 2.75;
      groundImages.slice(0, floorImageCount).forEach((item, index) => {
        const texture = textureLoader.load(item.dataUri);
        texture.colorSpace = THREE.SRGBColorSpace;
        texture.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
        const material = new THREE.MeshBasicMaterial({
          map: texture,
          transparent: true,
          opacity: 0.72,
          depthWrite: false
        });
        const panel = new THREE.Mesh(new THREE.PlaneGeometry(panelWidth, panelDepth), material);
        panel.rotation.x = -Math.PI / 2;
        panel.position.set(floorImageCount === 1 ? 0 : index === 0 ? -2.55 : 2.55, -2.19, 0);
        panel.name = `Ground image - ${item.label}`;
        scene.add(panel);
        groundItems.push({ mesh: panel, material, texture });
      });
    }

    const grid = new THREE.GridHelper(10.4, 26, 0xb8afa1, 0xd6d0c6);
    grid.position.y = -2.16;
    grid.visible = showGrid;
    scene.add(grid);

    const modelGroup = new THREE.Group();
    scene.add(modelGroup);

    const sourceBox = new THREE.Box3(
      new THREE.Vector3(...modelData.summary.bounds.min),
      new THREE.Vector3(...modelData.summary.bounds.max)
    );
    const sourceSize = new THREE.Vector3();
    const sourceCenter = new THREE.Vector3();
    sourceBox.getSize(sourceSize);
    sourceBox.getCenter(sourceCenter);
    const maxDim = Math.max(sourceSize.x, sourceSize.y, sourceSize.z, 1);
    const fitScale = 4.3 / maxDim;
    modelGroup.scale.setScalar(fitScale);
    modelGroup.position.set(-sourceCenter.x * fitScale, -sourceCenter.y * fitScale, -sourceCenter.z * fitScale);

    const meshItems: Array<{ mesh: THREE.Mesh; direction: THREE.Vector3 }> = [];
    modelData.meshes.forEach((packed: PackedMesh, index: number) => {
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.Float32BufferAttribute(packed.position, 3));
      if (packed.normal.length === packed.position.length) {
        geometry.setAttribute("normal", new THREE.Float32BufferAttribute(packed.normal, 3));
      } else {
        geometry.computeVertexNormals();
      }
      geometry.setIndex(packed.index);
      geometry.computeBoundingBox();
      geometry.computeBoundingSphere();

      const color = new THREE.Color(packed.color[0], packed.color[1], packed.color[2]);
      const material = new THREE.MeshStandardMaterial({
        color,
        metalness: index % 3 === 0 ? 0.34 : 0.18,
        roughness: 0.42,
        wireframe
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.name = packed.name;
      mesh.castShadow = true;
      mesh.receiveShadow = true;

      const localCenter = new THREE.Vector3(...packed.bounds.center);
      const direction = localCenter.clone().sub(sourceCenter);
      if (direction.lengthSq() < 0.000001) {
        direction.set(Math.sin(index + 1), Math.cos(index + 2), Math.sin(index * 0.7 + 0.4));
      }
      direction.normalize();
      modelGroup.add(mesh);
      meshItems.push({ mesh, direction });
    });

    const resize = () => {
      const box = host.getBoundingClientRect();
      const width = Math.max(320, Math.floor(box.width));
      const height = Math.max(320, Math.floor(box.height));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    };

    const setView = (view: ViewMode) => {
      const poses: Record<ViewMode, [number, number, number]> = {
        home: [7.2, 4.6, 7.8],
        front: [0, 1.2, 9.2],
        top: [0.1, 10.5, 0.1],
        detail: [3.3, 2.0, 4.1]
      };
      const [x, y, z] = poses[view];
      camera.position.set(x, y, z);
      controls.target.set(0, 0, 0);
      controls.update();
    };

    const api: SceneApi = {
      setView,
      reset: () => {
        setView("home");
        controls.reset();
      },
      capture: () => {
        const url = renderer.domElement.toDataURL("image/png");
        const link = document.createElement("a");
        link.href = url;
        link.download = `${viewerConfig.screenshotName || "product-interactive-3d-view"}.png`;
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    };
    onApi(api);

    const render = () => {
      const currentFlags = flagsRef.current;
      controls.autoRotate = currentFlags.autoRotate;
      grid.visible = currentFlags.showGrid;
      const explodeDistance = currentFlags.explode * 0.72;
      meshItems.forEach(({ mesh, direction }) => {
        mesh.position.copy(direction).multiplyScalar(explodeDistance);
        const material = mesh.material as THREE.MeshStandardMaterial;
        if (material.wireframe !== currentFlags.wireframe) {
          material.wireframe = currentFlags.wireframe;
          material.needsUpdate = true;
        }
      });
      controls.update();
      renderer.render(scene, camera);
      stateRef.current!.frame = window.requestAnimationFrame(render);
    };

    stateRef.current = { renderer, camera, controls, scene, modelGroup, meshItems, groundItems, grid, frame: 0 };
    resize();
    render();
    window.addEventListener("resize", resize);

    return () => {
      window.removeEventListener("resize", resize);
      onApi(null);
      const current = stateRef.current;
      if (current) {
        window.cancelAnimationFrame(current.frame);
        current.controls.dispose();
        current.renderer.dispose();
        current.meshItems.forEach(({ mesh }) => {
          mesh.geometry.dispose();
          (mesh.material as THREE.Material).dispose();
        });
        current.groundItems.forEach(({ mesh, material, texture }) => {
          mesh.geometry.dispose();
          material.dispose();
          texture.dispose();
        });
        host.removeChild(current.renderer.domElement);
      }
      stateRef.current = null;
    };
  }, [onApi]);

  return <div className="viewer-canvas" ref={hostRef} aria-label={`${productTitle} interactive 3D model`} />;
}

export default function App() {
  const [autoRotate, setAutoRotate] = useState(true);
  const [wireframe, setWireframe] = useState(false);
  const [showGrid, setShowGrid] = useState(true);
  const [explode, setExplode] = useState(0);
  const [sceneApi, setSceneApi] = useState<SceneApi | null>(null);

  const generatedDate = useMemo(() => {
    const date = new Date(modelData.summary.generatedAt);
    return Number.isNaN(date.getTime()) ? "to be confirmed" : date.toLocaleDateString("en-US");
  }, []);

  return (
    <div className="site-shell">
      <header className="site-header">
        <a className="brand" href={viewerConfig.brand?.url || "https://www.smthelp.com"} target="_blank" rel="noreferrer">
          <img src={logoDataUri} alt={`${viewerConfig.brand?.name || "Southern Machinery"} logo`} />
        </a>
        <nav className="header-actions" aria-label="Primary actions">
          {downloads.step ? (
            <button type="button" onClick={() => makeDownload(downloads.step)}>
              <Download size={17} />
              <span>{viewerConfig.downloads?.stepLabel || "STEP"}</span>
            </button>
          ) : null}
          {downloads.pdf ? (
            <button type="button" onClick={() => makeDownload(downloads.pdf)}>
              <Download size={17} />
              <span>{viewerConfig.downloads?.pdfLabel || "3D PDF"}</span>
            </button>
          ) : null}
          {downloads.native ? (
            <button type="button" onClick={() => makeDownload(downloads.native)}>
              <Download size={17} />
              <span>{viewerConfig.downloads?.nativeLabel || "CAD Source"}</span>
            </button>
          ) : null}
          <a href={viewerConfig.brand?.catalogUrl || "https://file.autoinsertion.com"} target="_blank" rel="noreferrer">
            <ExternalLink size={17} />
            <span>Catalog</span>
          </a>
        </nav>
      </header>

      <main className="viewer-stage">
        <section className="product-panel" aria-label="Product overview">
          <div className="eyebrow">
            <Box size={16} />
            <span>{companySlogan}</span>
          </div>
          <h1>{productTitle}</h1>
          <p>{sourceNotice}</p>
          <MarketingTiles />
        </section>

        <Viewer
          autoRotate={autoRotate}
          wireframe={wireframe}
          explode={explode}
          showGrid={showGrid}
          onApi={setSceneApi}
        />

        <section className="tool-panel" aria-label="3D controls">
          <div className="tool-grid">
            <ControlButton
              active={autoRotate}
              icon={autoRotate ? <Pause size={17} /> : <Play size={17} />}
              label={autoRotate ? "Pause" : "Rotate"}
              onClick={() => setAutoRotate((value) => !value)}
            />
            <ControlButton
              active={wireframe}
              icon={<ScanSearch size={17} />}
              label="Wire"
              onClick={() => setWireframe((value) => !value)}
            />
            <ControlButton
              active={showGrid}
              icon={<Grid3X3 size={17} />}
              label="Grid"
              onClick={() => setShowGrid((value) => !value)}
            />
            <ControlButton
              icon={<Camera size={17} />}
              label="Shot"
              onClick={() => sceneApi?.capture()}
            />
          </div>

          <div className="view-row" aria-label="Preset camera views">
            <button type="button" onClick={() => sceneApi?.setView("home")}>
              <Target size={16} />
            </button>
            <button type="button" onClick={() => sceneApi?.setView("front")}>
              <View size={16} />
            </button>
            <button type="button" onClick={() => sceneApi?.setView("top")}>
              <Maximize2 size={16} />
            </button>
            <button type="button" onClick={() => sceneApi?.setView("detail")}>
              <RotateCw size={16} />
            </button>
            <button type="button" onClick={() => sceneApi?.reset()}>
              <RotateCcw size={16} />
            </button>
          </div>

          <label className="slider-row">
            <span>
              <Layers size={16} />
              Explode
            </span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.02"
              value={explode}
              onChange={(event) => setExplode(Number(event.target.value))}
            />
          </label>
        </section>

        <aside className="source-panel rfq-panel" aria-label="Required RFQ information">
          <div className="rfq-heading">
            <strong>RFQ Required Information</strong>
            <span>{rfqIntro}</span>
          </div>
          <div className="rfq-grid">
            {rfqItems.map((item, index) => (
              <article className="rfq-item" key={item.label}>
                <div>
                  {rfqIcons[index % rfqIcons.length]}
                  <strong>{item.label}</strong>
                </div>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </aside>
      </main>

      <footer className="site-footer">
        <div className="footer-inner">
          <strong>Connect with Southern Machinery</strong>
          <div className="footer-links">
            {(viewerConfig.footerLinks || []).map(([label, url]: [string, string]) => (
              <a key={url} href={url} target="_blank" rel="noreferrer">
                {label}
              </a>
            ))}
          </div>
          <p>
            Browse our machine catalog at{" "}
            <a href={viewerConfig.brand?.catalogUrl || "https://file.autoinsertion.com"} target="_blank" rel="noreferrer">
              file.autoinsertion.com
            </a>{" "}
            and find machine photos at{" "}
            <a href={viewerConfig.photoUrl || "https://ph.smthelp.com"} target="_blank" rel="noreferrer">
              ph.smthelp.com
            </a>
            .
          </p>
        </div>
      </footer>
    </div>
  );
}
