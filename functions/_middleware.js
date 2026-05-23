export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === "moviezone-22y.pages.dev") {
    url.hostname = "movieszone.shop";
    return Response.redirect(url.toString(), 301); 
  }
  return context.next();
}
