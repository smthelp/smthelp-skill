# AI 写作特征库（24 类）

来源：Wikipedia *Signs of AI writing*（WikiProject AI Cleanup）。按外贸 B2B 场景做了取舍与示例替换。

---

## 内容类

### 1. 过度强调意义与趋势
**识别词**：stands/serves as、a testament to、pivotal、key milestone、underscores the importance、reflects broader、evolving landscape、marks a shift、indelible mark
**改法**：删掉意义判断，只说事实。

### 2. 过度强调知名度
**识别词**：independent coverage、leading expert、renowned worldwide、active social media presence
**改法**：换成具体事实（年份、客户类型、认证）。

### 3. -ing 虚假深度尾巴
**识别词**：highlighting、underscoring、ensuring、reflecting、contributing to、fostering、encompassing、showcasing
**改法**：拆成独立短句。
> Before: The S-70LD inserts at 0.8 s per component, ensuring stable throughput.
> After: The S-70LD inserts at 0.8 s per component. Throughput stays stable because the STF1003 tube feeder keeps it fed.

### 4. 广告式语言
**识别词**：boasts、vibrant、groundbreaking、cutting-edge、world-class、state-of-the-art、unparalleled、seamless、robust
**改法**：换成可核对的描述。
> Before: a state-of-the-art solution
> After: a two-stage preheat design with independent top/bottom control

### 5. 模糊归因
**识别词**：Industry reports、Experts believe、Studies show、Observers have noted（且无出处）
**改法**：给出处，或者直接断言（自己有把握的事不需要假引用）。

### 6. 套路化的"挑战与展望"
**识别词**：Despite its…、faces several challenges、Future Outlook、Challenges and Legacy
**改法**：删掉整段，或换成具体问题 + 时间点。

---

## 语言与语法类

### 7. AI 高频词
additionally、align with、crucial、delve、emphasizing、enduring、enhance、fostering、garner、highlight（动词）、interplay、intricate/intricacies、key（形容词）、landscape（抽象）、leverage、moreover、pivotal、robust、seamless、showcase、tapestry、testament、underscore（动词）、valuable、vibrant

> 注意：`key`、`enhance`、`valuable` 在普通语境没问题，问题是**密度**。一段里出现 3 个以上就要处理。

### 8. 回避系动词
**识别词**：serves as、stands as、marks、represents、boasts、features、offers（替代 is/has）
> Before: The SUL460 serves as the downstream buffer.
> After: The SUL460 is the downstream buffer.

### 9. 否定并列
**识别词**：Not only… but also…、It's not just… it's…
> Before: It's not just a machine, it's a productivity revolution.
> After: It cuts two operators from the line.

### 10. 三段式堆砌
把概念强行凑成三个。
> Before: It delivers efficiency, reliability, and cost-effectiveness.
> After (S-7900): It holds ±0.05 mm placement accuracy across a full shift.
> After (S-3000): It holds defect rates under 500 PPM on radial taped components.
>
> ⚠️ 精度数字**必须绑定机型**：S-7900 = ±0.05 mm，S-7020T = ±0.015 mm，
> 供料器（STF1003）= ±0.5 mm。三者差 10–30 倍，写错机型=事故。

**工业例外**：技术参数并列不算（见 SKILL.md Step 3）。

### 11. 同义词轮换（优雅变体）
AI 为避免重复而不断换词，反而显得不自然。同一对象在一段内应保持同一名称。

### 12. 虚假范围
**识别**：`from X to Y` 中 X 与 Y 不在同一量纲。
> Before: from prototyping to high-volume automotive production
> 判断：这是真实范围则保留，夸大则收窄。

---

## 风格类

### 13. 破折号滥用
一段内两次以上。改成句号或逗号。

### 14. 加粗滥用
机械地把术语加粗。技术文档里加粗只用于**警告**和**关键参数**。

### 15. 行内标题式列表
`- **Throughput:** 12,000 CPH` 这种。改成连贯段落，或改为表格（参数表用表格是对的）。
注意：产能数字要**带机型**——`12,000 CPH` 是 S-7020T，`4,000 CPH` 是 S-7900，
`10,000–12,000 CPH` 是 S-3000。裸写一个 CPH 等于没说。

### 16. 标题首字母全大写
`## Strategic Negotiations And Global Partnerships` → `## Strategic negotiations and global partnerships`

### 17. Emoji
B2B 工业内容一律删除。

### 18. 弯引号
统一改成直引号 `"`。

---

## 沟通类

### 19. 聊天腔残留
**识别词**：I hope this helps、Certainly!、Of course!、You're absolutely right!、Would you like me to…、let me know
**改法**：删掉。邮件正文不写这些。

### 20. 知识截止免责
**识别词**：as of my last update、while specific details are limited、based on available information
**改法**：删掉，换成可核查的表述或标注待确认。

### 21. 谄媚语气
Great question!、That's an excellent point! → 直接回应内容。

### 22. 填充短语
| AI | 人 |
|---|---|
| In order to achieve this | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| has the ability to | can |
| It is important to note that | （删掉） |

### 23. 过度对冲
> Before: It could potentially possibly be argued that the machine might improve throughput.
> After: The S-3000 runs 10,000–12,000 CPH on radial taped parts, at under 500 PPM.
>
> 写法：把 `[X]` 换成**能在 term-bank 查到的具体数字 + 机型 + 工况**。
> 查不到就不写数字，直接说结论，不要为了去对冲而编一个量。

### 24. 空洞的积极结尾
> Before: The future looks bright as we continue our journey toward excellence.
> After: Send us your Gerber file and we'll return a capacity simulation within two business days.

---

## 完整示例

**Before（AI）**
> Our new wave soldering solution serves as a testament to our commitment to innovation. Moreover, it provides a seamless, robust, and powerful manufacturing experience—ensuring that your production goals are met efficiently. It's not just a machine, it's a revolution in PCB assembly. Industry experts believe this will have a lasting impact on the entire electronics manufacturing landscape.

**After（A 档，方案用）**
> The S-WS450 handles boards up to 450 mm wide, with preheat to 280 °C and a solder
> bath to 300 °C in a 460 kg pot. It is lead-free compatible and runs a dual-wave
> system. Paired with the SUL460 Magazine Unloader (≈30 s magazine change, 10–40 mm
> pitch indexing), it closes the THT loop without manual board handling.

> ⚠️ 注意上例**没有链速数字**——因为 S-WS450 的 conveyor speed 不在已确认清单内。
> A 档宁可少一个参数，也不能填来源不明的数字。链速按工艺确认后再补。

**After（C 档，LinkedIn 用）**
> Most wave soldering lines don't lose time in the solder pot. They lose it at the exit, where boards stack up waiting for someone to unload them. We stopped treating the unloader as an accessory and started shipping it as part of the machine.
