// export default {
//   async fetch(request, env) {
//     const url = new URL(request.url);

//     // Visitor counter API
//     if (url.pathname === "/api/visit") {
//       if (request.method !== "GET") {
//         return new Response("Method Not Allowed", { status: 405 });
//       }

//       // Increase the counter by 1
//       await env.DB
//         .prepare("UPDATE visits SET count = count + 1 WHERE id = 1")
//         .run();

//       // Read the updated counter
//       const result = await env.DB
//         .prepare("SELECT count FROM visits WHERE id = 1")
//         .first();

//       return Response.json({
//         count: result.count
//       });
//     }

//     // Everything else → serve your portfolio files
//     return env.ASSETS.fetch(request);
//   }
// };



export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle visitor counter API
    if (url.pathname === "/api/visit") {
      if (request.method !== "GET") {
        return new Response("Method Not Allowed", { status: 405 });
      }

      // READ ONLY — do not increment
      if (url.searchParams.has("read")) {
        const result = await env.DB
          .prepare("SELECT count FROM visits WHERE id = 1")
          .first();

        return Response.json({
          count: result.count
        });
      }

      // NORMAL VISIT — increment by 1
      await env.DB
        .prepare("UPDATE visits SET count = count + 1 WHERE id = 1")
        .run();

      const result = await env.DB
        .prepare("SELECT count FROM visits WHERE id = 1")
        .first();

      return Response.json({
        count: result.count
      });
    }

    // Serve your website
    return env.ASSETS.fetch(request);
  }
};