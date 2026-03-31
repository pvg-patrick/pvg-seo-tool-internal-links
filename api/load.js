const { S3Client, GetObjectCommand } = require("@aws-sdk/client-s3");

// Only allow simple relative JSON paths, no path traversal
const ALLOWED = /^[\w][\w\-/]*\.json$/;

module.exports = async (req, res) => {
  const file = (req.query.file || "").trim();

  if (!ALLOWED.test(file)) {
    return res.status(400).json({ error: "Invalid file parameter" });
  }

  const bucket = process.env.S3_BUCKET;
  const region = process.env.S3_REGION || "eu-central-1";
  const prefix = process.env.S3_PREFIX || "";

  if (!bucket) {
    return res.status(500).json({ error: "S3_BUCKET not configured" });
  }

  const s3 = new S3Client({
    region,
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
  });

  const key = prefix + file;

  try {
    const data = await s3.send(
      new GetObjectCommand({ Bucket: bucket, Key: key })
    );
    const body = await data.Body.transformToString("utf-8");
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "public, max-age=300");
    return res.status(200).send(body);
  } catch (err) {
    if (err.name === "NoSuchKey" || err.$metadata?.httpStatusCode === 404) {
      return res.status(404).json({ error: "File not found" });
    }
    console.error("[api/load]", err.message);
    return res.status(500).json({ error: "Failed to load file" });
  }
};
