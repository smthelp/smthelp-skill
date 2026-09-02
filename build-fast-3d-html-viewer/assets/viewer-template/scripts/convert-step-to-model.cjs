const fs = require("fs");
const path = require("path");
const occtImportJs = require("occt-import-js")();

const root = path.resolve(__dirname, "..");
const configPath = path.join(root, "viewer-config.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8").replace(/^\uFEFF/, ""));
const stepFile = config.source && config.source.step ? config.source.step : "model.stp";
const stepPath = path.join(root, "assets", stepFile);
const outPath = path.join(root, "src", "model-data.ts");

function flattenTriplets(value) {
  if (!Array.isArray(value)) return [];
  if (value.length === 0) return [];
  if (Array.isArray(value[0])) return value.flat();
  return value;
}

function roundList(value, digits = 5) {
  const factor = 10 ** digits;
  return value.map((item) => Math.round(Number(item) * factor) / factor);
}

function normalizeColor(color, index) {
  const palette = [
    [0.42, 0.46, 0.50],
    [0.18, 0.56, 0.62],
    [0.83, 0.55, 0.19],
    [0.50, 0.52, 0.56],
    [0.72, 0.25, 0.22],
    [0.25, 0.43, 0.66]
  ];
  if (Array.isArray(color) && color.length >= 3) {
    return roundList(color.slice(0, 3).map((item) => Math.max(0, Math.min(1, Number(item)))), 3);
  }
  return palette[index % palette.length];
}

function makeBox() {
  return {
    min: [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY],
    max: [Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY]
  };
}

function includePosition(box, x, y, z) {
  if (x < box.min[0]) box.min[0] = x;
  if (y < box.min[1]) box.min[1] = y;
  if (z < box.min[2]) box.min[2] = z;
  if (x > box.max[0]) box.max[0] = x;
  if (y > box.max[1]) box.max[1] = y;
  if (z > box.max[2]) box.max[2] = z;
}

function finalizeBox(box) {
  const size = [
    box.max[0] - box.min[0],
    box.max[1] - box.min[1],
    box.max[2] - box.min[2]
  ];
  const center = [
    (box.max[0] + box.min[0]) / 2,
    (box.max[1] + box.min[1]) / 2,
    (box.max[2] + box.min[2]) / 2
  ];
  return {
    min: roundList(box.min, 4),
    max: roundList(box.max, 4),
    size: roundList(size, 4),
    center: roundList(center, 4)
  };
}

async function main() {
  if (!fs.existsSync(stepPath)) {
    throw new Error(`STEP source not found: ${stepPath}`);
  }

  const occt = await occtImportJs;
  const fileContent = fs.readFileSync(stepPath);
  const params = {
    linearUnit: "millimeter",
    linearDeflectionType: "bounding_box_ratio",
    linearDeflection: 0.0032,
    angularDeflection: 0.65
  };
  const result = occt.ReadStepFile(new Uint8Array(fileContent), params);
  if (!result || !result.success) {
    throw new Error(`STEP import failed: ${JSON.stringify(result && result.error)}`);
  }

  const globalBox = makeBox();
  let vertexCount = 0;
  let triangleCount = 0;

  const meshes = result.meshes
    .map((mesh, index) => {
      const position = roundList(flattenTriplets(mesh.attributes && mesh.attributes.position && mesh.attributes.position.array), 3);
      const indices = flattenTriplets(mesh.index && mesh.index.array).map((item) => Number(item));

      if (position.length < 9 || indices.length < 3) {
        return null;
      }

      const meshBox = makeBox();
      for (let i = 0; i < position.length; i += 3) {
        includePosition(meshBox, position[i], position[i + 1], position[i + 2]);
        includePosition(globalBox, position[i], position[i + 1], position[i + 2]);
      }

      vertexCount += position.length / 3;
      triangleCount += indices.length / 3;

      return {
        name: `Mesh ${index + 1}`,
        color: normalizeColor(mesh.color, index),
        position,
        normal: [],
        index: indices,
        bounds: finalizeBox(meshBox)
      };
    })
    .filter(Boolean);

  const summary = {
    source: stepFile,
    generatedAt: new Date().toISOString(),
    meshCount: meshes.length,
    vertexCount,
    triangleCount,
    bounds: finalizeBox(globalBox),
    note: "Fast visual/layout mesh generated from STEP with reduced tessellation and computed normals. Final dimensions, machine compatibility, and commercial specifications are to be confirmed."
  };

  const source = `/* Auto-generated from assets/${stepFile}. Do not edit by hand. */
export type PackedMesh = {
  name: string;
  color: [number, number, number];
  position: number[];
  normal: number[];
  index: number[];
  bounds: {
    min: [number, number, number];
    max: [number, number, number];
    size: [number, number, number];
    center: [number, number, number];
  };
};

export type PackedModel = {
  summary: {
    source: string;
    generatedAt: string;
    meshCount: number;
    vertexCount: number;
    triangleCount: number;
    bounds: {
      min: [number, number, number];
      max: [number, number, number];
      size: [number, number, number];
      center: [number, number, number];
    };
    note: string;
  };
  meshes: PackedMesh[];
};

export const modelData: PackedModel = ${JSON.stringify({ summary, meshes })};
`;

  fs.writeFileSync(outPath, source, "utf8");
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
