import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { Search } from 'lucide-react';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { mockTools, featuredTools, categories } from '../mockData';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [priceFilter, setPriceFilter] = useState('All');
  const [sortBy, setSortBy] = useState('Name');

  const filteredTools = useMemo(() => {
    let filtered = mockTools;

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(tool => 
        tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Category filter
    if (categoryFilter && categoryFilter !== 'All') {
      filtered = filtered.filter(tool => tool.category === categoryFilter);
    }

    // Price filter
    if (priceFilter && priceFilter !== 'All') {
      filtered = filtered.filter(tool => tool.pricing === priceFilter);
    }

    // Sort
    if (sortBy === 'Name') {
      filtered = [...filtered].sort((a, b) => a.name.localeCompare(b.name));
    }

    return filtered;
  }, [searchQuery, categoryFilter, priceFilter, sortBy]);

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500 text-white py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <Link to="/" className="inline-flex items-center gap-3 mb-8 hover:opacity-80 transition-opacity">
            <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
              <div className="text-2xl font-bold text-purple-600">AI</div>
            </div>
            <div className="text-left">
              <div className="text-xl font-bold">AI BOX 4U</div>
              <div className="text-xs opacity-90">DIRECTORY</div>
            </div>
          </Link>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-4">AI Tools Directory</h1>
          <p className="text-xl md:text-2xl mb-12 opacity-95">The world's best curated list of AI Tools</p>
          
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Search AI tool or category"
                className="w-full pl-12 pr-4 py-6 text-lg rounded-lg text-gray-900"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          
          <div className="mt-8 flex gap-4 justify-center">
            <Button className="bg-black hover:bg-gray-900 text-white px-6 py-3 rounded-lg">
              <Link to="/submit">Submit Tool</Link>
            </Button>
            <Button className="bg-white text-black hover:bg-gray-100 px-6 py-3 rounded-lg">
              <Link to="/admin">Advertise</Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Featured Tools Section */}
      {featuredTools.length > 0 && (
        <div className="max-w-7xl mx-auto px-4 py-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {featuredTools.map((tool, index) => (
              <div key={tool.id} className="text-center">
                <h3 className="text-lg font-semibold mb-4">Featured Tool: <span className="font-bold">{tool.name}</span></h3>
                <Link to={`/tool/${tool.id}`}>
                  <img 
                    src={tool.image} 
                    alt={tool.name}
                    className="w-full h-64 object-cover rounded-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer"
                  />
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters Section */}
      <div className="bg-gray-50 border-y border-gray-200 py-6">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="bg-white">
                <SelectValue placeholder="Sort by Name" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Name">Name</SelectItem>
              </SelectContent>
            </Select>

            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="bg-white">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map(cat => (
                  <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={priceFilter} onValueChange={setPriceFilter}>
              <SelectTrigger className="bg-white">
                <SelectValue placeholder="Price" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All</SelectItem>
                <SelectItem value="Free">Free</SelectItem>
                <SelectItem value="Paid">Paid</SelectItem>
                <SelectItem value="Freemium">Freemium</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTools.map(tool => (
            <Card key={tool.id} className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group">
              <Link to={`/tool/${tool.id}`}>
                <img 
                  src={tool.image} 
                  alt={tool.name}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </Link>
              <CardContent className="p-6">
                <Link to={`/tool/${tool.id}`}>
                  <h3 className="text-xl font-bold mb-2 hover:text-purple-600 transition-colors">{tool.name}</h3>
                </Link>
                
                <div className="flex gap-2 mb-3">
                  <Badge variant="secondary" className="bg-teal-500 text-white hover:bg-teal-600">
                    {tool.category}
                  </Badge>
                </div>
                
                <div className="flex flex-wrap gap-1 mb-3">
                  {tool.tags.map((tag, idx) => (
                    <Badge key={idx} variant="outline" className="text-xs bg-green-100 text-green-800 border-green-300">
                      {tag}
                    </Badge>
                  ))}
                </div>
                
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">{tool.description}</p>
                
                <div className="flex items-center justify-between">
                  <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200">{tool.pricing}</Badge>
                  <Link to={`/tool/${tool.id}`}>
                    <Button className="bg-pink-600 hover:bg-pink-700 text-white">Details</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {filteredTools.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No tools found matching your criteria.</p>
          </div>
        )}
      </div>

      {/* Scroll to Top Button */}
      <button
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        className="fixed bottom-8 right-8 bg-gray-800 text-white p-4 rounded-full shadow-lg hover:bg-gray-900 transition-colors"
        aria-label="Scroll to top"
      >
        ↑
      </button>
    </div>
  );
};

export default Home;
