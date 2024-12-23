## MicrosoftAuthenticator TOTP to Canokey/Yubikey

用于批量、快速迁移 TOTP 到 Canokey 中（或 Yubikey）。

### 数据库准备

1. 在一台有 ROOT 的 Android 设备上登录 Microsoft Authenticator 软件，并完成数据同步。
2. 使用文件管理工具，访问 `/data/data/com.azure.authenticator/databases/PhoneFactor`。
3. 将 `PhoneFactor`、`PhoneFactor-shm`、`PhoneFactor-wal`（如果存在后两个则复制）复制到 PC 上，放到脚本所在的目录下。
4. （可能需要）在电脑上，使用 [SQLiteStudio](https://github.com/pawelsalawa/sqlitestudio) 或其他工具打开一次 `PhoneFactor` 数据库，以解决一些缓存和同步的问题。

### 环境配置

1. 安装 [Python](https://www.python.org/)。

2. 安装 `ckman`：

   ```bash
   pip install canokey-manager
   ```

3. 配置下面的环境变量

   `DB_PATH`：PhoneFactor 数据库的位置。

   `CANOKEY_PIN`：TOTP 应用的 Pin 码。


### 使用

#### 正常启动：

```bash
python main.py
```

运行过程中，如果 `ckman` 返回值不是 1 的条目（意味着可能出现错误），程序会暂停，并向用户确认是否继续导入剩余条目。

运行完成后，会将上述”可能出错“条目，加入到一个 `error_list` 中，并存为 `error_list.txt` 文件，请注意该文件包含密钥。

#### 错误重试：

在运行时添加命令行参数：`-r` 或 `--retry-error`：

```bash
python main.py -r
```

与正常启动相比，唯一区别在于：程序将会读取 `error_list.txt`  作为数据来源，而不是从数据库中读取。

随后的行为与正常启动完全一致，包括再次更新错误列表。

### 其他

对于 Yubikey，请安装 [yubikey-manager](https://developers.yubico.com/yubikey-manager/) 的 CLI 版本：

```bash
pip install --user yubikey-manager
```

然后自行修改代码，将其中的 `ckman` 更换为 `ykman`。

