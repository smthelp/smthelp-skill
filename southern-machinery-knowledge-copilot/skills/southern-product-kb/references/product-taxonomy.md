# Southern Machinery 产品分类体系

## 7 大产品类别（标准定义）

所有 Southern Machinery 产品必须归入以下 7 类之一，不得自创分类。

### 1. SMT（表面贴装）
**定义**：用于 PCB 表面贴装工艺的设备，包括贴片主机与 SMT 产线配套设备。
**归属规则**：
- 贴片机（Pick & Place）→ SMT
- 回流焊（Reflow Oven）→ SMT
- AOI（自动光学检测）→ SMT
- 钢网清洗机（Stencil Cleaner）→ SMT
- 吸嘴清洗机（Nozzle Cleaner）→ SMT
- 锡膏搅拌机（Solder Paste Mixer）→ SMT
- EDA/ESD 料架（ESD Rack）→ SMT

**代表型号**：S-600SV、S-530SV、S-V8

### 2. THT（通孔插装）
**定义**：用于 PCB 通孔插装工艺的设备，包括自动插件机与异形插件机。
**归属规则**：
- 自动径向插件机 → THT
- 自动轴向插件机 → THT
- 异形插件机（Odd-form）→ THT
- 焊锡机器人（Solder Robot）→ THT

**代表型号**：S-70LD、S-3000、S-4000、S7020

### 3. Wave Soldering（波峰焊）
**定义**：用于 THT 元件波峰焊接工艺的设备，及波峰焊后处理设备。
**归属规则**：
- 波峰焊机（Wave Soldering）→ Wave Soldering
- PCBA 清洗机（PCBA Cleaning）→ Wave Soldering
- 锡渣分离机（Solder Unloader/dross）→ Wave Soldering

### 4. Board Handling（板处理）
**定义**：用于 PCB 在产线各工位间传输、缓存、翻转的设备。
**归属规则**：
- 上板机（Loader）→ Board Handling
- 下板机（Unloader）→ Board Handling
- 缓存机（Buffer）→ Board Handling
- 传送带（Conveyor）→ Board Handling
- 翻板机（Flipper）→ Board Handling
- 翻转机（Inverter）→ Board Handling
- 平移传送带（Translational Conveyor）→ Board Handling

### 5. Peripheral（周边设备）
**定义**：辅助主工艺设备完成产线自动化的配套设备，不属于上述 4 类的辅助设备。
**归属规则**：
- 清洁类辅助设备 → Peripheral
- 物料管理类辅助设备 → Peripheral
- 其他辅助自动化设备 → Peripheral

### 6. Accessory（配件）
**定义**：安装于主机上、随主机运行的可更换部件，非独立设备。
**归属规则**：
- Feeder（供料器）→ Accessory
- Nozzle（吸嘴）→ Accessory
- Tray Feeder（盘式供料器）→ Accessory
- Tube Feeder（管式供料器）→ Accessory
- Radial / Axial / Odd-form Feeder → Accessory

### 7. Spare Part（耗材）
**定义**：产线运行中消耗、需定期补充的物料。
**归属规则**：
- 焊锡条 / 焊锡丝 / 焊锡膏 → Spare Part
- 清洗剂 → Spare Part
- 网板 → Spare Part
- 其他消耗品 → Spare Part

## 分类判定优先级

1. 先看设备是否独立运行：独立运行 → 1-5 类；安装在主机上 → Accessory；消耗品 → Spare Part。
2. 再看主工艺：贴片/回流/检测 → SMT；通孔插装 → THT；波峰焊接 → Wave Soldering；板传输 → Board Handling；辅助 → Peripheral。
3. 边界情况：锡膏搅拌机既可归 SMT 也可归 Peripheral，优先归 SMT（与主工艺绑定）。

## 多类归属处理

一台设备只归一类。若看似跨类（如 Solder Robot 既涉及 THT 又涉及焊接），归入其**主工艺**类别，并在知识卡片"关联设备"章节标注跨工艺关联。
