# Human challenge

## 介绍
### demo
[点击访问](https://hc.winefox.cc/)

### 这是什么？
这是一个简单的小工具 可以让对方进行一次人机验证

### 使用场景举例
- 在社交平台私聊时，发给疑似机器人的对方，要求对方提供验证码。
- 在进入私密群组前，要求用户完成挑战并提供 JWT 凭证。

### 它的工作原理是什么？
当有人访问的时候 它会要求其做一个 hCaptcha 挑战，如果成功就会返回一个验证码，然后你可以在这个网站上查询验证码的真伪

### 它的效果如何
不敢保证绝对有效 重要操作请通过多种渠道确认！

不敢保证绝对有效 重要操作请通过多种渠道确认！

不敢保证绝对有效 重要操作请通过多种渠道确认！

### 技术栈
使用全栈框架 Django 开发

## 安装
建议使用 Docker 安装 
```bash
git clone https://github.com/linyuyuan2010/human-challenge.git
docker compose up
```

不出意外的话 docker 会报错 因为还没配置 `.env`

打开挂载的 `data` 目录

将`.env.example`重命名为`.env`

打开并填写完里面的内容

#### Django 配置
| 变量名 | 必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| DJANGO_SECRET_KEY | 是 |-| Django 项目的唯一密钥，用于加密签名。建议使用随机字符串。 |
| DEBUG_MODE | 否 | False | 是否开启调试模式。生产环境请务必设为 False。 |
| ALLOW_HOSTS | 是| localhost | "允许访问的域名，多个域名用英文逗号 `,` 分隔。 |
| CSRF_TRUSTED_HOSTS | 是 | - | 信任的 CSRF 来源，必须包含协议头（如 `https://hc.example.com`）多个域名用英文逗号 `,` 分隔。 |


#### Redis 配置
| 变量名 | 必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| REDIS_HOST | 是 | - | Redis 服务器地址（比如`redis://127.0.0.1:6379/1`）。 |
| REDIS_PASSWORD | 否 | - | Redis 连接密码。 |


#### hCaptcha 配置
需要前往 [hCaptcha 官网](https://dashboard.hcaptcha.com/) 获取

| 变量名 | 必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| HCAPTCHA_SITEKEY | 是 | - | hCaptcha 的 Site Key。 |
| HCAPTCHA_SECRETKEY | 是 | - | hCaptcha 的 Secret Key。 |


#### JWT 配置
| 变量名 | 必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| JWT_PRIVATE_KEY_PATH | 否 | - | 私钥文件路径（相对于 /data/ 目录，如 keys/private.pem）。 |
| JWT_PUBLIC_KEY_PATH | 否 | - | 公钥文件路径（相对于 /data/ 目录，如 keys/public.pem）。 |
| ISSUER | 否 | example.com | JWT 签发者名称，建议填写你的域名。 |
| EXPIRING_IN | 否 | 300 | JWT 令牌有效期，单位为秒（默认 5 分钟）。 |

## JWT模式
*下文中所有`hc.winefox.cc`如果自托管的话可以替换为你的域名*

使用 JWT 模式的具体细节

0. 你需要生成一个 nonce，长度适中，太长会影响回调，太短不够安全，建议 7-8 位字母/数字混合为宜，为了防止重放和伪造受众攻击。

1. 拼接 URL 并将用户重定向 `https://hc.winefox.cc/jwt/?sub=<用户标识符，以你能看得懂为宜>&aud=<密钥受众，建议使用你的域名>&method=<回调方法，post或者get 留空则为get>&nonce=<第1步生成的nonce>&callback=<你的回调url>`。

2. 用户完成操作后 此工具会将用户重定向至第2步时的回调url 验证结果将以 `id` 参数（post模式也是`id`）传达。例如: `https://example.com/?id=<验证结果，标准JWT>`

3. 验证 JWT 使用的是 `ES256` 算法签名 其公钥在 `https://hc.winefox.cc/.well-known/jwks.json` 可用。返回体格式为标准 JWKS。
    - *另外 有一个非标准接口：`https://hc.winefox.cc/api/public-key/` 提供但不建议使用 此接口将直接返回 pem 格式公钥。*

4. 解码 JWT 验签后 注意一定要校验 `iss` `aud` `nonce` 字段，`nonce` 字段和第一步生成的应该相同。

JWT 的载荷格式为
```json
{
  "sub": "在第2步中传入的sub字段",
  "aud": "在第2步中传入的aud字段",
  "iss": "hc.winefox.cc",
  "exp": <过期时间>,
  "iat": <颁发时间>,
  "nonce": "在第1步中生成以及第2步中传入的nonce",
  "jti": "对于此jwt随机生成的唯一标识符",
  "verified": True,  # 用布尔值代表是否通过验证
}
```


## Q&A

Q0: 怎么得到密钥对

A0: 可以利用 openssl 生成 生成私钥：`openssl ecparam -name prime256v1 -genkey -noout -out private.pem` 生成公钥：`openssl ec -in private.pem -pubout -out public.pem`


Q1: 验证码的有效期是多久

A1: 普通模式默认为 60 秒，JWT 模式默认为 5 分钟
