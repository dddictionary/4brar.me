INSERT IGNORE INTO hobbies (title, description, source) VALUES
('Soccer', 'Whether it''s a pickup game or watching a match, soccer has always been my go-to sport. Nothing beats the flow of a good game.', 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=500&h=500&fit=crop'),
('Rock Climbing', 'Bouldering is my favorite way to problem-solve off the keyboard. Every route is a puzzle that demands both strength and strategy.', 'https://images.unsplash.com/photo-1522362485439-83fcff4673f0?w=500&h=500&fit=crop'),
('Driving', 'Long drives with good music are underrated. There''s something about the open road that clears the mind.', 'https://images.unsplash.com/photo-1449965408869-ebd13bc9e5a8?w=500&h=500&fit=crop'),
('Coding', 'Building things in my free time is how I stay sharp and explore new ideas. This website is one of those projects.', 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500&h=500&fit=crop');

INSERT IGNORE INTO work_experiences (title, role, startdate, enddate, description) VALUES
('Shopify', 'Engineering Intern', 'Sep 2025', 'Present', 'Led Tier 1 migration of transactional messaging pipeline from single-region to dual-region using Kubernetes overlay architecture. Developed static analysis tooling that identified 40+ security vulnerabilities across 330K+ lines of Ruby code.'),
('Meta', 'Production Engineering Fellow', 'Jun 2025', 'Sep 2025', 'Deployed containerized web application using Docker and Nginx reverse proxy for production workloads. Implemented monitoring and alerting stack with Prometheus and Grafana.'),
('ACM CCNY', 'Backend Engineer & Teaching Assistant', 'Jun 2024', 'Aug 2025', 'Built fault-tolerant Node.js backend handling 10GB+ across 5+ databases with automated daily backups. Led team of 5 to deliver MERN MVP in 8 weeks using sprint planning and agile workflows.');

INSERT IGNORE INTO education (title, startdate, enddate, description) VALUES
('CUNY City College of New York', 'Aug 2022', 'Dec 2025', 'Bachelor of Science in Computer Science. Relevant coursework in Data Structures, Algorithms, Operating Systems, Computer Networks, and Database Systems.');

INSERT IGNORE INTO locations (name, lat, lng) VALUES
('Paris, France', 48.8566, 2.3522),
('New York, USA', 40.7128, -74.0060),
('Tokyo, Japan', 35.6895, 139.6917),
('London, UK', 51.5074, -0.1278),
('Los Angeles, USA', 34.0522, -118.2437),
('São Paulo, Brazil', -23.5505, -46.6333),
('Cairo, Egypt', 30.0444, 31.2357),
('Dubai, UAE', 25.2048, 55.2708),
('Istanbul, Turkey', 41.0082, 28.9784),
('Bangkok, Thailand', 13.7563, 100.5018),
('Seoul, South Korea', 37.5665, 126.9780),
('Sydney, Australia', -33.8688, 151.2093),
('Mexico City, Mexico', 19.4326, -99.1332);
