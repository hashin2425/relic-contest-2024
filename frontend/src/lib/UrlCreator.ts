const apiUrl = (() => {
  let tempApiUrl = process.env.NEXT_PUBLIC_API_URL || "";
  if (tempApiUrl.endsWith("/")) {
    tempApiUrl = tempApiUrl.slice(0, -1);
  }
  return tempApiUrl;
})();

export default function urlCreator(target: string): string {
  if (!target.startsWith("/")) {
    target = "/" + target;
  }
  return apiUrl + target;
}
