# 示例输入 / Example input — S-JVF02

## Jason 的请求（2026-10-31，摘要）
基于 JUKI RS-1 震动飞达 S-JVF02 的产品资料，生成中英文各一份《出厂验收 Checklist》：覆盖外观与结构、机构装配与螺丝紧固、飞达供料与振动/皮带机构、传感器与光电检测、电气与安全（接地、绝缘、急停）、规格参数核对（型号、电压、频率、适用元件范围）；每项含编号、检查项目、验收标准（量化）、检查方法、判定结果、记录栏；中英一一对应，术语统一（飞达=Feeder、振动=Vibration、供料=Feeding），品牌与型号不翻译；资料无法访问或缺失须说明并标注推测项。

## 资料清单
| ID | 类型 | 资料 | 读取结果 |
|---|---|---|---|
| MAN | 操作手册 PDF（14 页，Rev. 2025） | https://file.autoinsertion.com/public/Southern%20Machinery%20SMT%20Product%20Operation%20Manual/Southern-Machinery-S-JVF02-SMT-Stick-Vibration-Feeder-Operation-Manual-2025.pdf | 可读；p.2 无文字层（目录页）；§3 明确写“未给出电气参数、尺寸、重量” |
| WEB | 产品页 HTML | https://file.autoinsertion.com/public/Product%20landing%20Page/s-jvf02-vibration-stick-feeder-juki-rs-1.html | 可读；§03 规格表提供电压、功率、尺寸、重量、料道、元件范围 |
| 3D | 3D 图纸页 ×4 | https://file.autoinsertion.com/public/SMT%20machine%203D%20Drawing%20in%20Html/ （RS-1 Vibration Feeder S-JVF02.html 等） | 结构展示，无新增参数，未作来源 |
| AUD | 音频 WAV | https://file.autoinsertion.com/public/SMT%20Audio/S-JVF02%20Vibration%20Stick%20Feeder%20RS-1.wav | 营销讲解，未取参数 |

## 提取结果（事实表）
| 类别 | 事实 | 值 | 来源 |
|---|---|---|---|
| 技术参数 | 型号 | S-JVF02 | 手册 封面 p.1；§3 p.6 |
| 技术参数 | 适配机型 | JUKI RS-1 飞达座 | 产品页 §03 'Model compatibility' |
| 电气指标 | 电压 | 24 V DC | 产品页 §03 'Voltage' |
| 电气指标 | 功率 | 15 W | 产品页 §03 'Power' |
| 技术参数 | 料道数 | 4 条独立 | 产品页 §03 'Input channels' |
| 技术参数 | 适用元件 | 3 × 3 mm – 30 × 10 mm | 产品页 §03 'Component size range' |
| 技术参数 | 料管宽度 | 66 mm | 产品页 §03 'Stick width' |
| 尺寸公差 | 外形尺寸 | 365 × 66 × 125 mm（无公差） | 产品页 §03 'Overall size' |
| 尺寸公差 | 重量 | 6.5 kg（无公差） | 产品页 §03 'Weight' |
| 功能项 | 频率 / 功率两个旋钮，指示灯，开关 | — | 手册 §2.2 p.5；§5.2 p.9 |
| 装配 | 安装 4 步：抬手柄、对定位孔、对连接器、放手柄锁定 | — | 手册 §4.1 p.7–8 |
| 装配 | 料管三点固定：定位环、板簧、定位块；取料区切开顶面 | — | 手册 §5.1 p.9 |
| 安全 | 抬手柄装拆；锁定后再开机；关开关再拆装/换料管；手远离取料区 | — | 手册 §1 p.3 |
| 附件备件 | 14 项零件 S-JVF02-052801 ~ 052814 | — | 手册 §9 p.12 |
| 功能项 | 故障排除 4 条（指示灯不亮、送料慢、跳料、取不到料） | — | 手册 §8 p.11 |
| 缺失 | 振动频率范围、公差、扭矩、电气测试阈值、噪音、传感器、警示标签、包装 | — | 资料未给出 → S 或 T |

## 归类 → 分区
功能项 / 供料 → C；技术参数 → F；外观 / 尺寸 → A；装配 → B；安全 / 电气 → E；指示灯 / 开关 / 识别 → D；附件备件 → A05 + F08。
