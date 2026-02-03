# 🎨 Frontend-Only Docker Testing Guide

This guide helps you test the SequoAlpha frontend independently using Docker.

## 🚀 Quick Start

```bash
# Run the automated test script
./test-frontend-only.sh
```

This will:
1. Build the frontend Docker image
2. Start the frontend container on port 9000
3. Test if it's responding
4. Open http://localhost:9000 in your browser

## 📋 What This Tests

✅ **HTML rendering** - Main page loads correctly  
✅ **CSS styling** - All styles applied  
✅ **JavaScript loading** - React components load  
✅ **Static files** - Images, fonts, etc.  
✅ **Nginx configuration** - Server setup works  
✅ **Responsive design** - Mobile/desktop layouts  

❌ **NOT tested** - Backend API calls (will show errors, this is expected)

## 🔧 Manual Commands

### Build Frontend Image

```bash
docker build -f Dockerfile.frontend-only -t sequoalpha-frontend-test .
```

### Run Frontend Container

```bash
docker run -d \
  --name sequoalpha-frontend-only \
  -p 9000:80 \
  sequoalpha-frontend-test
```

### View Logs

```bash
docker logs -f sequoalpha-frontend-only
```

### Stop Container

```bash
docker stop sequoalpha-frontend-only
```

### Remove Container

```bash
docker rm sequoalpha-frontend-only
```

### Clean Restart

```bash
docker stop sequoalpha-frontend-only
docker rm sequoalpha-frontend-only
docker rmi sequoalpha-frontend-test
./test-frontend-only.sh
```

## 🌐 Access Points

- **Frontend URL**: http://localhost:9000
- **Nginx status**: Container logs show server status

## 🧪 What You Can Test

### ✅ Frontend Features (Work Without Backend)

1. **Page Layout**
   - Landing page displays correctly
   - Header/footer/navigation visible
   - Images and logos load
   - Responsive design works

2. **CSS/Styling**
   - Colors and fonts correct
   - Animations work
   - Hover effects functional
   - Media queries responsive

3. **JavaScript (Limited)**
   - React components mount
   - UI interactions (buttons, menus)
   - Client-side routing (if any)
   - Form validation (client-side)

### ❌ Backend Features (Will NOT Work)

1. **Authentication**
   - Login will fail (no backend)
   - Session management disabled
   - JWT token validation fails

2. **API Calls**
   - Document uploads fail
   - User creation fails
   - Data fetching fails
   - All `/api/*` endpoints return 404

3. **Database Operations**
   - No data persistence
   - No user accounts
   - No document storage

## 📊 Expected Behavior

### What You Should See

✅ Landing page loads  
✅ Styles are applied correctly  
✅ Images display  
✅ Navigation renders  
✅ React components mount  

### Expected Errors (Normal)

❌ API connection errors in console  
❌ "Failed to fetch" messages  
❌ 404 errors for `/api/*` endpoints  
❌ Authentication failures  

**These errors are EXPECTED and NORMAL** when testing frontend-only.

## 🔍 Debugging

### Container Won't Start

```bash
# Check if port 9000 is in use
lsof -i :9000

# Check Docker logs
docker logs sequoalpha-frontend-only

# Inspect container
docker inspect sequoalpha-frontend-only
```

### Page Shows 404

```bash
# Check nginx configuration
docker exec sequoalpha-frontend-only cat /etc/nginx/conf.d/default.conf

# Check if files are copied
docker exec sequoalpha-frontend-only ls -la /usr/share/nginx/html/
```

### Styles Not Loading

```bash
# Check CSS files exist
docker exec sequoalpha-frontend-only ls -la /usr/share/nginx/html/css/

# Check nginx access log
docker logs sequoalpha-frontend-only | grep css
```

### JavaScript Errors

Open browser console (F12) and check:
- Are scripts loading?
- Any CORS errors? (should be none for static files)
- React errors?

## 🎯 Testing Workflow

### 1. Visual Testing

```bash
./test-frontend-only.sh
# Open http://localhost:9000
# Check:
# - Landing page looks correct
# - Navigation works
# - Images display
# - Responsive design
```

### 2. Browser Console Testing

```bash
# Open browser console (F12)
# Check for:
# - JavaScript errors (ignore API errors)
# - CSS loading issues
# - Resource 404s (except /api/*)
```

### 3. Network Tab Testing

```bash
# Open Network tab (F12)
# Check:
# - index.html loads (200)
# - All CSS files load (200)
# - All JS files load (200)
# - Images load (200)
# - API calls fail (404) - this is expected
```

### 4. Responsive Testing

```bash
# In browser:
# - Open DevTools (F12)
# - Click device toolbar (Ctrl+Shift+M)
# - Test different screen sizes
# - Check mobile/tablet/desktop layouts
```

## 📝 Development Workflow

### Making Changes to Frontend

1. **Edit frontend files**:
   ```bash
   nano index.html
   # or
   nano frontend/js/App.js
   # or
   nano css/main.css
   ```

2. **Rebuild and test**:
   ```bash
   docker stop sequoalpha-frontend-only
   docker rm sequoalpha-frontend-only
   ./test-frontend-only.sh
   ```

3. **Refresh browser** to see changes

### Live Development (Alternative)

For faster development without Docker rebuild:

```bash
# Just serve files with Python
python3 -m http.server 9001
# Open http://localhost:9001
```

## 🔄 Integration with Full Stack

Once frontend looks good:

### Test with Backend

```bash
# Stop frontend-only
docker stop sequoalpha-frontend-only

# Start full stack
docker-compose up -d

# Test at http://localhost:8080
```

### Test on EC2

After deploying to EC2:
1. Frontend files go to `/home/ubuntu/sequoalpha/`
2. Nginx serves them
3. Backend API proxied through nginx

## 📊 Comparison

| Feature | Frontend-Only | Full Stack (docker-compose) | EC2 Production |
|---------|---------------|---------------------------|----------------|
| **Port** | 9000 | 8080 | 80/443 |
| **Backend** | ❌ No | ✅ Yes | ✅ Yes |
| **Database** | ❌ No | ✅ Yes | ✅ Yes |
| **API Calls** | ❌ Fail | ✅ Work | ✅ Work |
| **Use Case** | UI testing | Full testing | Production |

## 🎨 Frontend Files Structure

```
/usr/share/nginx/html/
├── index.html              ← Main page
├── frontend/
│   └── js/
│       ├── App.js          ← Main React component
│       ├── Login.js        ← Login component
│       ├── Dashboard.js    ← Admin dashboard
│       ├── UserDashboard.js
│       ├── DocumentCenter.js
│       └── config.js       ← API configuration
├── css/
│   ├── main.css
│   └── landing.css
├── images/                 ← Logo, icons, etc.
└── *.png                   ← Favicon files
```

## 🚦 Status Indicators

### Container Healthy
```bash
$ docker ps
NAME                       STATUS
sequoalpha-frontend-only   Up 2 minutes (healthy)
```

### Container Unhealthy
```bash
$ docker ps
NAME                       STATUS
sequoalpha-frontend-only   Up 2 minutes (unhealthy)
```

Check logs: `docker logs sequoalpha-frontend-only`

## 💡 Tips

1. **Use browser DevTools** - Essential for debugging
2. **Ignore API errors** - Expected without backend
3. **Test responsive** - Different screen sizes
4. **Check console** - For JavaScript errors
5. **Use Network tab** - See what's loading
6. **Test on mobile** - Use device emulation
7. **Clear cache** - Hard refresh (Ctrl+Shift+R)

## 🆚 vs Full Stack Testing

### Use Frontend-Only When:
- ✅ Testing UI/UX changes
- ✅ Checking responsive design
- ✅ Verifying static files load
- ✅ Testing CSS changes
- ✅ Quick visual feedback
- ✅ No backend needed

### Use Full Stack (docker-compose) When:
- ✅ Testing API integration
- ✅ Testing authentication
- ✅ Testing data flow
- ✅ Testing file uploads
- ✅ End-to-end testing
- ✅ Before deploying to EC2

## 🎯 Success Criteria

Frontend-only test is successful when:

✅ Container starts without errors  
✅ http://localhost:9000 loads  
✅ Landing page displays correctly  
✅ All images load (no broken images)  
✅ Styles are applied (colors, fonts correct)  
✅ Navigation is visible  
✅ No 404 errors for static files  
✅ Responsive design works  

❌ API errors in console are **EXPECTED and OK**

## 📞 Troubleshooting

### Port 9000 Already in Use

```bash
# Find what's using it
lsof -i :9000

# Use different port in test-frontend-only.sh
# Change -p 9000:80 to -p 9001:80
```

### Container Exits Immediately

```bash
# Check logs
docker logs sequoalpha-frontend-only

# Common causes:
# - Nginx config error
# - Missing files
# - Port conflict
```

### Files Not Found (404)

```bash
# Verify files were copied
docker exec sequoalpha-frontend-only ls -la /usr/share/nginx/html/

# Check build output
docker build -f Dockerfile.frontend-only -t sequoalpha-frontend-test .
```

## 🎉 Next Steps

After successful frontend testing:

1. ✅ Frontend looks good → Test full stack
2. ✅ Full stack works → Deploy to EC2
3. ✅ EC2 deployed → Test in production
4. ✅ Production works → You're done! 🎊

---

**Happy Testing!** 🎨
