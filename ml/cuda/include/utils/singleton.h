#ifndef UTILS_SINGLETON_H_
#define UTILS_SINGLETON_H_

#include <type_traits>

template<typename T>
class Singleton {
 public:
  static T &getInstance() noexcept(std::is_nothrow_constructible<T>::value) {
    static T instance;
    return instance;
  }

  virtual ~Singleton() noexcept {};

  Singleton(const Singleton &) = delete;
  Singleton &operator=(const Singleton &) = delete;

 protected:
  Singleton() {}
};

#endif// !UTILS_SINGLETON_H_