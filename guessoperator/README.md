## 这只干员有点神秘

### 

### 警告

这个插件的配置要求有**亿丶丶麻烦**，且**对于性能和网络环境**有着一定**要求**，请谨慎选择。

本功能不支持私聊，因为每轮猜干员都需要创建一个浏览器实例，为了确保性能，故只能在群聊中进行。

如果长时间未响应或者出现报错，极大概率为网络问题导致，可以过段时间再尝试。

后续会进行重构以提高性能和友好性( 总之，现版本请谨慎尝试。 因为只是个人写作娱乐的(逃

### 配置要求

#### 基本依赖项

本插件依赖于Nonebot2 beta2和[nonebot_adapter_mirai2适配器](https://github.com/ieew/nonebot_adapter_mirai2)，如果您不是，需要自行修改源代码相关mirai2适配器内容。

当然如果都不是Nb2，~~那已经无能为力了×~~

同时需要Nonebot2官方提供的定时任务插件，[NoneBot Plugin APScheduler](https://github.com/nonebot/plugin-apscheduler)

#### Selenium配置

依照于目前的实现，本插件实际上是一种自动化程序，每次指令都会指示浏览器操作后完成截图，我们需要Selenium，后续会重构为playwright，这将更加稳定。

+ 安装Selenium

```python
pip install selenium
```

+ 浏览器和相关Driver

既然使用了Selenium，我们同时还需要配置浏览器Driver

这里使用的是Microsoft Edge，安装此浏览器，然后去[这里](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)按照版本和系统安装Driver

> 如果不想用Edge，可以使用其他浏览器，方法一样，然后更改[此行代码](https://github.com/RainChain-Zero/Jasmine_Nonebot2_Plugins_Center/blob/beb0a30adcc65ff47c5f57c1a69130f4b7496a14/guessoperator/__init__.py#L54)以创建当前浏览器实例

#### 插件配置

您应当将guesoperator文件夹作为整体使用，放入bot安装插件处后，更改[这行](https://github.com/RainChain-Zero/Jasmine_Nonebot2_Plugins_Center/blob/beb0a30adcc65ff47c5f57c1a69130f4b7496a14/guessoperator/__init__.py#L94)和[这行](https://github.com/RainChain-Zero/Jasmine_Nonebot2_Plugins_Center/blob/beb0a30adcc65ff47c5f57c1a69130f4b7496a14/guessoperator/__init__.py#L220)文件路径，指向operator.json文件。

> 提示：为了保证正确的干员识别，每次方舟更新新角色需要按照该文件内格式进行干员增加，可以去[原网站](http://akg.saki.cc)找到正确的信息。

当然了，该文件是为了确保正确的干员识别，因为网络原因，时不时会出现识别不出干员名的情况，如果您对自己的网络状况有自信，可以删去相关代码并修改[此部分](https://github.com/RainChain-Zero/Jasmine_Nonebot2_Plugins_Center/blob/beb0a30adcc65ff47c5f57c1a69130f4b7496a14/guessoperator/__init__.py#L75)。



### 使用指令

之后启动Nb2即可，关于指令的使用说明可以看[这里](https://rainchain-zero.github.io/JasmineDoc/manual/nonebot2/guessoperator.html)。

如果需要更改回复内容，比如机器人名，需要修改对应代码部分。

