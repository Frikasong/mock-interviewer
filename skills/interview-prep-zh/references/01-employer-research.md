# Step 1 — 调研岗位

目标：把「他们是谁、他们要什么」变成三个可被反复引用的文件。

---

## 1. 逐行拆 JD

JD 每一条职责后面都藏着一道题。逐条读，倒推 1-2 个考点，输出一张对照表。

| JD 原文 | 它在考什么 | 可能的问法 |
|---|---|---|
| Manage relationships with internal and external stakeholders | 跨部门协调、处理分歧 | Tell me about a time you had to push back on a senior stakeholder. |
| Work in a fast-paced environment with competing deadlines | 优先级判断、抗压 | You have three deadlines on the same day. Walk me through how you'd triage. |
| Draft submissions and correspondence | 书面能力、受众意识 | How do you adjust your writing for a non-legal audience? |

同时注意 JD 的**动词层级**：support / assist 类岗位考的是可靠和学习速度；lead / own / develop 类岗位考的是判断和责任。答题的重心要跟着变。

还要留意 JD 里的**反常项**——一条和岗位主体关系不大的要求（比如一个后台岗写了"public-facing communication"），往往是团队真实痛点，问到的概率反而高。

## 2. 公司档案 company-dossier.md

用联网搜索，覆盖：

- **主营业务与收入/资金结构**（政府或监管机构则写：法定授权来源、监管对象、经费来源）
- **组织结构**：这个岗位在哪个部门、向谁汇报、这个部门做什么
- **最近 12 个月关键动态**：产品发布 / 财报 / 人事变动 / 监管或行业变化 / 战略文件（政府机构看 business plan、annual report、statement of priorities）
- **JD 里的职责分别对应哪些真实业务线**
- **区别于同行的 3 个具体特点**——这一条单独回答，是 Why Them 的原料

每条信息标日期和来源链接。记忆里的东西不写进档案；不确定的标 `[未证实]`。

配合搜索的 prompt：

```
帮我调研 [公司/机构名]：主营业务与组织结构；最近 12 个月的关键动态
（产品发布 / 财报 / 人事 / 监管或行业变化）；这个 job posting 里列的职责
分别对应它哪些真实业务。输出 markdown 供存档，每条标注来源和日期。
最后单独回答：这家机构区别于同行的 3 个具体特点。
```

## 3. Why Them 三层论证 why-them.md

不要抄官网价值观，不要说"贵司行业领先、文化很好"。三层：

**第一层：我的轨迹为什么指向这里**
过去的选择连成一条线，终点自然落在这个岗位上。用事实而不是形容词——修过什么课、做过什么项目、在哪实习过、写过什么。

**第二层：我对它业务/方向的判断**
你读了它的年报/战略文件/最近的监管动向，你有一个具体看法。这是最能拉开差距的一层，因为绝大多数候选人只到第一层。看法不必标新立异，但必须具体到能被追问。

**第三层：我具体想参与它什么工作**
指名道姓某个部门、某条业务线、某个正在推进的项目，说清楚你能贡献什么。

**检验**：把机构名遮掉，这段话还能不能用在它的竞争对手身上？能，就重写。

## 4. 题库 question-bank.md

来源：
- JD 倒推题（上面第 1 步的产出，最靠谱）
- 公开面经：Glassdoor、一亩三分地、Reddit、LinkedIn 上该机构员工的公开分享
- 行业/岗位类型通用题库
- 直接问学长学姐、校友、该机构现员工（最准，鼓励用户去问）
- 该机构自己公布的招聘流程说明（政府和监管机构常常公开 competency framework，照着准备命中率极高）

分四类归档：

- **动机类**：why this role / why us / why leave / 职业规划
- **行为类**：tell me about a time…（用 STAR 答）
- **情景类**：what would you do if…（先给判断框架再给结论）
- **公司专属**：只有这家会问的（业务理解、法定职能、近期事件看法、技术/专业笔试）

格式必须严格，Mock Interviewer 直接解析这个文件：

```markdown
### Tell me about a time you disagreed with a supervisor.
- type: 行为
- budget: 120s
- best story: S03
- backup: S07
- opener: I raised it early, in writing, and framed it as a risk to the file rather than a disagreement.
- watch: 背景不要超过两句
```
